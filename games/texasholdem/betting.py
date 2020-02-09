from games.texasholdem.interfaces.status import GameInput

__author__ = "Ferenc Fazekas"


class BettingRound:
    def __init__(self, player_chips: [int], big_blind_index: int, big_blind_amount: int, players_in: [bool]) -> None:
        self.player_chips = player_chips
        self.big_blind_index: int = big_blind_index
        self.big_blind_amount: int = big_blind_amount
        self.current_bet_amount: int = big_blind_amount
        self.current_player: int = self.big_blind_index
        self.players_in: [bool] = players_in
        self.bets: [int] = [0] * len(players_in)
        self.folded: [bool] = [None] * len(players_in)
        self.checked: [bool] = [False] * len(players_in)

    def get_next_player(self) -> int:
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
            if potential_prev is len(self.players_in):
                potential_prev = 0
            if self.players_in[potential_prev]:
                return potential_prev

    def check(self):
        self.current_player = self.get_next_player()
        self.checked[self.current_player] = True

    def bet(self, amount: int):
        self.current_player = self.get_next_player()
        self.player_chips[self.current_player] -= amount
        self.bets[self.current_player] = amount

    def fold(self):
        self.current_player = self.get_next_player()
        self.players_in[self.current_player] = False
        self.folded[self.current_player] = False
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
        return NotImplemented

    def get_pot(self):
        pot: int = 0
        for bet in self.bets:
            pot += bet
        return pot

    def process_input_descriptor(self, input_descriptor: GameInput):
        action = input_descriptor.action
        amount = input_descriptor.amount
        print("Invoking action <{}> with params <{}>.".format(action, amount))
        # todo refactor to enum or constants
        if action is "bet":
            self.bet(amount)
        elif action is "call":
            self.call_bet()
        elif action is "check":
            self.check()
        elif action is "fold":
            self.fold()
        elif action is "raise":
            self.raise_bet(amount)
