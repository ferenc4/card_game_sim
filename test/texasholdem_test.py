import unittest

from games.texasholdem.texasholdem import TexasHoldem, BettingRound


class TestStringMethods(unittest.TestCase):
    def test_all_bet_once(self):
        first_player = 0
        players = 8
        starter_chips = 100
        game = TexasHoldem(players, starter_chips=starter_chips, seed=8)
        game.deal_hands()

        b1 = BettingRound(game.player_chips, first_player, game.big_blind, game.players_with_chips())
        b1.bet(20)
        for i in range(first_player, first_player + players - 1):
            b1.call_bet()
        game.betting(b1)

        game.flop()
        game.turn()
        game.river()
        game.print_status()
        game.finalise()
        game.print_status()
        expected_winners = [1]
        for i in range(0, len(game.player_chips)):
            chips = game.player_chips[i]
            if i in expected_winners:
                self.assertGreater(chips, starter_chips)
            else:
                self.assertLess(chips, starter_chips)


if __name__ == '__main__':
    unittest.main()
