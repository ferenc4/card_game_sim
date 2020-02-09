__author__ = "Ferenc Fazekas"

import unittest

from games.texasholdem.texasholdem import TexasHoldem, BettingRound, RandomDeck


class TestStringMethods(unittest.TestCase):
    def test_pair(self):
        self.single_bet_test([1], 8)

    # change the seed for a different outcome
    def single_bet_test(self, expected_winners, seed=1, first_player=0, players=8, starter_chips=100):
        game = TexasHoldem(players, starter_chips=starter_chips, deck=RandomDeck(seed))
        game.deal_hands()
        b1 = BettingRound(game.player_chips, first_player, game.big_blind_amount, game.players_with_chips())
        b1.bet(20)
        for i in range(first_player, first_player + players - 1):
            b1.call_bet()
        game.conduct_betting_round(b1)
        game.flop()
        game.turn()
        game.river()
        game.print_status()
        game.finalise()
        game.print_status()
        for i in range(0, len(game.player_chips)):
            chips = game.player_chips[i]
            if i in expected_winners:
                self.assertGreater(chips, starter_chips)
            else:
                self.assertLess(chips, starter_chips)


if __name__ == '__main__':
    unittest.main()
