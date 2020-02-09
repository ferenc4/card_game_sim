from collections import namedtuple

from games.texasholdem.interfaces.status import GameStatus, GameInput
from games.texasholdem.texasholdem import TexasHoldem, FrontEnd


class ConsoleInterface(FrontEnd):
    def wait_for_input(self, status: GameStatus) -> GameInput:
        actions = ["bet", "raise", "call", "fold", "check"]
        print("Player {}'s turn.".format(status.current_player))
        action = input("Please input an action that matches one of {}: ".format(actions))
        amount = None
        if action in ["bet", "raise"]:
            amount = int(input("Please input an amount: ".format(actions)))
        return GameInput(action, amount)


def run():
    """
    Terminal view is considered debug mode,
    and as a result will contain minimal
    input sensitisation.
    """
    players = int(input("How many players are playing?"))
    if players < 2 or players > 8:
        raise ValueError("Player count has to be between 2 and 8 incl., but was {}."
                         .format(players))
    print("Starting game with {} players.".format(players))
    game = TexasHoldem(ConsoleInterface(), players)
    game.deal_hands()
    # todo add betting round here
    game.flop()
    # todo add betting round here
    game.turn()
    # todo add betting round here
    game.river()
    game.print_status()
    game.conduct_betting_round()
    game.finalise()
    game.print_status()
