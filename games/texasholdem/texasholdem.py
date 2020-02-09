from dataclasses import dataclass
from typing import NamedTuple

from cards.deck import Card, RandomDeck
from games.texasholdem.betting import BettingRound
from games.texasholdem.interfaces.status import GameStatus, ChipStatus, CheckedStatus, CardNumberStatus, CardSuitStatus, \
    FoldedStatus, CardPositionIdentifier

__author__ = "Ferenc Fazekas"


class FrontEnd:
    def wait_for_input(self, status: GameStatus):
        raise NotImplementedError()


@dataclass
class HandAnalysis:
    weight: int
    five_card_hand: [Card]


@dataclass
class WinnersDetails:
    winners: [int]
    analyses: [HandAnalysis]


class TexasHoldem:
    def __init__(self,
                 front_end: FrontEnd,
                 player_count: int,
                 starter_chips=100,
                 chip_to_blind_ratio=50,
                 deck=RandomDeck()) -> None:
        self.player_hands: [Card] = [None] * player_count
        self.shared: [Card] = [None] * 5
        self.deck: [Card] = deck
        self.pot_size: int = 0
        self.player_chips: [int] = [starter_chips] * player_count
        self.chip_to_blind_ratio: int = chip_to_blind_ratio
        self.betting_rounds: [BettingRound] = []
        self.big_blind_amount = int(starter_chips / chip_to_blind_ratio)
        self.current_big_blind = 0
        self.front_end = front_end

    def deal_hands(self) -> None:
        for i in range(0, self.player_hands.__len__()):
            self.player_hands[i] = [self.deck.draw(), self.deck.draw()]

    def reveal(self, index: int) -> None:
        self.shared[index] = self.deck.draw()

    def flop(self) -> None:
        for i in range(0, 3):
            self.reveal(i)

    def turn(self) -> None:
        self.reveal(3)

    def river(self) -> None:
        self.reveal(4)

    def conduct_betting_round(self):
        players_in = self.players_with_chips() if len(self.betting_rounds) is 0 else self.betting_rounds[-1].players_in
        cur_round = BettingRound(self.player_chips, self.current_big_blind, self.big_blind_amount, players_in)
        for player_i, is_player_in in enumerate(players_in):
            if is_player_in:
                status = self.status_for(player_i, cur_round)
                input_desc = self.front_end.wait_for_input(status)
                cur_round.process_input_descriptor(input_desc)
        self.betting_rounds.append(cur_round)

    def players_in(self):
        return self.betting_rounds[len(self.betting_rounds) - 1].players_in

    def finalise(self):
        winners_details = self.allocate_winner()
        self.pot_size = 0
        for betting_round in self.betting_rounds:
            self.pot_size += betting_round.get_pot()
        self.allocate_pot(winners_details.analyses, winners_details.winners)
        self.betting_rounds = []
        self.rotate_big_blind()

    def allocate_winner(self) -> WinnersDetails:
        best_analyses = []
        winners: [int] = []
        for index, current_player in enumerate(self.player_hands):
            if self.players_in()[index]:
                new_analysis: HandAnalysis = get_best_hand(current_player, self.shared)
                if len(best_analyses) > 0:
                    # todo compare to all current best analyses to see if one is worse than the rest
                    comparison = compare_hands(best_analyses[0], new_analysis)
                    if comparison == 1:
                        winners = [index]
                        best_analyses = [new_analysis]
                    elif comparison == 0:
                        winners.append(index)
                        best_analyses.append(new_analysis)
                else:
                    best_analyses.append(new_analysis)
        return WinnersDetails(winners, best_analyses)

    def allocate_pot(self, best_analyses, winners):
        print("Winners are:")
        analysis_i = 0
        for winner in winners:
            full_hand = best_analyses[analysis_i]
            starting_hand = self.player_hands[winner]
            print("Player {} won. SH: {} FH: {}".format(winner + 1, starting_hand, full_hand))
            self.player_chips[winner] += self.pot_size / len(winners)
            analysis_i += 1

    def rotate_big_blind(self):
        proposed_big_blind = (self.current_big_blind + 1) % len(self.player_hands)
        players_in = self.players_with_chips()
        while proposed_big_blind not in players_in:
            proposed_big_blind = (proposed_big_blind + 1) % len(self.player_hands)
        self.current_big_blind = proposed_big_blind

    def status_for(self, player_index: int, betting_round: BettingRound):
        checked_statuses = None
        folded_statuses = None
        suit_statuses = None
        number_statuses = None
        chip_statuses: [ChipStatus] = [ChipStatus(i, v) for i, v in enumerate(self.player_chips)]
        checked_statuses: [CheckedStatus] = betting_round.checked
        folded_statuses: [FoldedStatus] = betting_round.folded
        if self.player_hands:
            suit_statuses = []
            number_statuses = []
            for player_i, hand in enumerate(self.player_hands):
                for card_i, card in enumerate(hand):
                    cpi = CardPositionIdentifier(player_i, card_i)
                    suit_statuses.append(CardSuitStatus(cpi, card.suit))
                    number_statuses.append(CardSuitStatus(cpi, card.number))
        return GameStatus(player_index,
                          chip_statuses,
                          checked_statuses,
                          folded_statuses,
                          suit_statuses,
                          number_statuses)
        # to track:
        # p{playerIndex}IsPlaying: Bool
        # p{playerIndex}Chips: Bool
        # t[PreFlop, Flop, Turn, River]P{playerIndex}Checked: Bool
        # t[PreFlop, Flop, Turn, River]P{playerIndex}Folded: Bool
        # t[PreFlop, Flop, Turn, River]P{playerIndex}[Bet, Call, Raise]Amount: int
        # cardIndex 1-5 + 8(1-2) Other players are none until reveal
        # p{playerIndex}Card{cardIndex}Suit: Enum
        # p{playerIndex}Card{cardIndex}Number: Enum

    def print_status(self):
        print("\n")
        for i in range(0, self.player_hands.__len__()):
            current_player = self.player_hands[i]
            chips = self.player_chips[i]
            print("Player {}: {:>4} {:>4} ${} ({} BB)".format(i + 1,
                                                              str(current_player[0]),
                                                              str(current_player[1]),
                                                              str(chips),
                                                              str(chips / self.big_blind_amount)))
        print("Board: ", end="")
        for i in range(0, self.shared.__len__()):
            if self.shared[i]:
                current_shared: str = str(self.shared[i])
                print("{:5}".format(current_shared), end="")
        print("\n")

    def players_with_chips(self):
        players_with_chips: [bool] = []
        for chips in self.player_chips:
            if chips > 0:
                players_with_chips.append(True)
            else:
                players_with_chips.append(False)
        return players_with_chips


def highcard_analysis(reverse_cards: [Card], count=5) -> [Card]:
    return reverse_cards[:count]


def one_pair_analysis(reverse_cards: [Card]) -> [Card]:
    return n_of_a_kind(reverse_cards, 2)


def three_of_a_kind_analysis(reverse_cards: [Card]) -> [Card]:
    return n_of_a_kind(reverse_cards, 3)


def four_of_a_kind_analysis(reverse_cards: [Card]) -> [Card]:
    return n_of_a_kind(reverse_cards, 4)


def straight_analysis(reverse_cards: [Card]) -> [Card]:
    cards: [Card] = reverse_cards.copy()
    if reverse_cards[0].number == 14:
        cards.append(reverse_cards[0])
    current_streak: [Card] = []
    for card in cards:
        if len(current_streak) is not 5:
            if len(current_streak) == 0 or current_streak[len(current_streak) - 1].number < card.number:
                current_streak = [card]
            elif current_streak[len(current_streak) - 1].number > card.number:
                current_streak.append(card)
    if len(current_streak) is 5:
        return current_streak
    else:
        return None


def flush_analysis(reverse_cards: [Card]) -> [Card]:
    suits = dict()
    for card in reverse_cards:
        suit_ary = []
        if suits.__contains__(card.suit):
            suit_ary = suits.get(card.suit)
        suit_ary.append(card)
        if len(suit_ary) is 5:
            return suit_ary
        suits[card.suit] = suit_ary
    return None


def n_of_a_kind(reverse_cards, threshold):
    current_streak: [Card] = []
    for card in reverse_cards:
        if len(current_streak) < threshold:
            if len(current_streak) is 0 or current_streak[0].number is card.number:
                current_streak.append(card)
            else:
                current_streak = [card]
        if len(current_streak) is threshold:
            # exclude the cards in the streak from the high cards
            filtered = list(filter(lambda a: a.number != current_streak[0].number, reverse_cards))
            tiebreakers = highcard_analysis(filtered, 5 - threshold)
            current_streak.extend(tiebreakers)
            return current_streak
    return None


def get_best_hand(hand: [Card], board: [Card]) -> HandAnalysis:
    visible = list(hand)
    visible.extend(board)
    visible.sort(key=lambda it: (it.number + 13) % 14, reverse=True)
    analysis_functs = [
        straight_analysis,
        flush_analysis,
        four_of_a_kind_analysis,
        three_of_a_kind_analysis,
        one_pair_analysis,
        highcard_analysis
    ]
    for index, analysis_funct in enumerate(analysis_functs):
        result: [Card] = analysis_funct(visible)
        if result is not None:
            return HandAnalysis(len(analysis_functs) - index, result)
    raise ValueError("Hand analysis failed. High card hand should always apply.")


# assumes hands are sorted in reverse order of winning (high to low)
def compare_hands(analysis1: HandAnalysis, analysis2: HandAnalysis) -> int:
    if analysis1.weight > analysis2.weight:
        return -1
    if analysis1.weight < analysis2.weight:
        return 1
    if len(analysis1.five_card_hand) is not len(analysis2.five_card_hand):
        raise ValueError("Expected hand sizes to match, but they were of size {} and {}."
                         .format(analysis1.five_card_hand, analysis2.five_card_hand))
    for card_index in range(0, len(analysis1.five_card_hand)):
        card1 = analysis1.five_card_hand[card_index]
        card2 = analysis2.five_card_hand[card_index]
        if card1.number > card2.number:
            return -1
        elif card1.number < card2.number:
            return 1
    return 0
