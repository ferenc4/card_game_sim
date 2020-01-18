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
        self.assertGreater(game.player_chips[0], starter_chips)
        self.assertGreater(game.player_chips[1], starter_chips)
        self.assertGreater(game.player_chips[2], starter_chips)
        self.assertGreater(game.player_chips[3], starter_chips)
        self.assertLess(game.player_chips[4], starter_chips)
        self.assertLess(game.player_chips[5], starter_chips)
        self.assertLess(game.player_chips[6], starter_chips)
        self.assertGreater(game.player_chips[7], starter_chips)
        self.assertLess(game.player_chips[8], starter_chips)


if __name__ == '__main__':
    unittest.main()
