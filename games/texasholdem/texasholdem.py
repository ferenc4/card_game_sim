from cards.deck import Deck, Card
from games.texasholdem.hands import HIGH_CARD, ONE_PAIR


class BettingRound:
    def __init__(self, player_chips: [int], big_blind_index: int, big_blind_amount: int, players_in: [bool]) -> None:
        self.player_chips = player_chips
        self.big_blind_index = big_blind_index
        self.big_blind_amount = big_blind_amount
        self.current_bet_amount = big_blind_amount
        self.current_player = big_blind_index - 1
        self.players_in = players_in
        self.bets = []
        for is_player_in in players_in:
            if is_player_in:
                self.bets.append(0)
            else:
                self.bets.append(None)

    def get_next_player(self):
        potential_next = self.current_player
        found_next = False
        while not found_next:
            potential_next += 1
            if potential_next == len(self.players_in):
                potential_next = 0
            if self.players_in[potential_next]:
                return potential_next

    def get_prev_player(self):
        potential_prev = self.current_player
        found_prev = False
        while not found_prev:
            potential_prev += 1
            if potential_prev == len(self.players_in):
                potential_prev = 0
            if self.players_in[potential_prev]:
                return potential_prev

    def check(self):
        self.current_player = self.get_next_player()

    def bet(self, amount: int):
        self.current_player = self.get_next_player()
        self.player_chips[self.current_player] -= amount
        self.bets[self.current_player] = amount

    def fold(self):
        self.current_player = self.get_next_player()
        self.players_in[self.current_player] = False
        print('{} folded.'.format(str(self.current_player)))

    def call_bet(self):
        self.current_player = self.get_next_player()
        bet_to_match = max(self.bets)
        additional = bet_to_match - self.bets[self.current_player]
        allin_or_match = self.player_chips[self.current_player] if additional > self.player_chips[self.current_player] \
            else additional
        print('{} matching bet {} with {}'.format(str(self.current_player), str(bet_to_match),
                                                  str(additional + self.bets[self.current_player])))
        self.player_chips[self.current_player] -= allin_or_match
        self.bets[self.current_player] += allin_or_match

    def raise_bet(self, amount):
        bet_to_raise_on = max(self.bets)
        if amount < bet_to_raise_on:
            raise Exception("Invalid raise, because amount <{}> is less than a previous bet <{}>.".format(
                amount,
                bet_to_raise_on
            ))
        self.current_player = self.get_next_player()
        actual_raise = amount - self.bets[self.current_player]
        print('{0} raising to {1}'.format(str(self.current_player), str(actual_raise)))
        if actual_raise <= 0:
            raise Exception("Invalid raise amount <{}> for previous bet <{}>.".format(amount,
                                                                                      self.bets[self.current_player]))
        self.player_chips[self.current_player] -= actual_raise
        self.bets[self.current_player] = actual_raise

    def is_finished(self) -> bool:
        return self.is_one_player_standing() and self.do_unmatched_bets_exist()

    def is_one_player_standing(self):
        found_player_standing = False
        for is_player_in in self.players_in:
            if is_player_in:
                if found_player_standing:
                    # Found 2 players are still playing
                    return False
                found_player_standing = True
        return True

    def print_all(self):
        for i in range(0, len(self.player_chips)):
            print(str(self.player_chips[i]) + " " + ("I" if self.players_in[i] else "O"), " ")
        print()
        for bet in self.bets:
            print(bet, " ")
        print()

    def do_unmatched_bets_exist(self) -> bool:
        return True

    def get_pot(self):
        pot: int = 0
        for bet in self.bets:
            pot += bet
        return pot


class TexasHoldem:
    def __init__(self, player_count: int, starter_chips=100, chip_to_blind_ratio=50, seed=None) -> None:
        self.players = [None] * player_count
        self.shared = [None] * 5
        self.deck = Deck(seed)
        self.pot_size = 0
        self.player_chips = [starter_chips] * player_count
        self.chip_to_blind_ratio = chip_to_blind_ratio
        self.betting_rounds = []
        self.big_blind = starter_chips / chip_to_blind_ratio

    def deal_hands(self):
        for i in range(0, self.players.__len__()):
            self.players[i] = [self.deck.draw(), self.deck.draw()]

    def reveal(self, index):
        self.shared[index] = self.deck.draw()

    def flop(self):
        for i in range(0, 3):
            self.reveal(i)

    def turn(self):
        self.reveal(3)

    def river(self):
        self.reveal(4)

    def betting(self, round: BettingRound):
        self.betting_rounds.append(round)

    def players_in(self):
        return self.betting_rounds[len(self.betting_rounds) - 1].players_in

    def finalise(self):
        best_analyses = []
        winners: [int] = []
        for index, current_player in enumerate(self.players):
            if self.players_in()[index]:
                new_analysis = hand_analysis(current_player, self.shared)
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
        self.pot_size = 0
        for betting_round in self.betting_rounds:
            self.pot_size += betting_round.get_pot()
        print("Winners are:")
        analysis_i = 0
        for winner in winners:
            full_hand = best_analyses[analysis_i]
            starting_hand = self.players[winner]
            print("Player {} won. SH: {} FH: {}".format(winner + 1, starting_hand, full_hand))
            self.player_chips[winner] += self.pot_size / len(winners)
        self.betting_rounds = []

    def status(self):
        print("\n")
        for i in range(0, self.players.__len__()):
            current_player = self.players[i]
            chips = self.player_chips[i]
            print("Player {}: {:>4} {:>4} ${} ({} BB)".format(i + 1,
                                                              str(current_player[0]),
                                                              str(current_player[1]),
                                                              str(chips),
                                                              str(chips / self.big_blind)))
        print("Board: ", end="")
        for i in range(0, self.shared.__len__()):
            if self.shared[i]:
                current_shared: str = str(self.shared[i])
                print("{:5}".format(current_shared), end="")
        print("\n")

    def players_with_chips(self):
        players_with_chips = []
        for player in self.player_chips:
            players_with_chips.append(player > 0)
        return players_with_chips


def highcard_analysis(sorted_cards: [Card]) -> [Card]:
    return sorted_cards[:5]


def one_pair_analysis(sorted_cards: [Card]) -> [Card]:
    current_card: Card = None
    for card in sorted_cards:
        if current_card and current_card.number is card.number:
            return [current_card, card]
        current_card = card
    return None


def hand_analysis(hand: [Card], board: [Card]) -> [[Card]]:
    visible = list(hand)
    visible.extend(board)
    visible.sort(key=lambda it: (it.number + 13) % 14, reverse=True)
    analysis = [
        one_pair_analysis(visible),
        highcard_analysis(visible)
    ]
    return analysis


def compare_hands(analysis1: [[Card]], analysis2: [[Card]]):
    len1 = len(analysis1)
    len2 = len(analysis2)
    if len1 is not len2:
        raise Exception("Cannot compare analyses with different lengths <{}> and <{}>.".format(len1, len2))
    for i in range(0, len1):
        hand1 = analysis1[i]
        hand2 = analysis2[i]
        if hand1 and not hand2:
            return -1
        if hand2 and not hand1:
            return 1
    return 0
