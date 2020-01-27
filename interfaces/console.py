from games.texasholdem.texasholdem import BettingRound, TexasHoldem


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
    game = TexasHoldem(players)
    game.deal_hands()
    # todo add betting round here
    game.flop()
    # todo add betting round here
    game.turn()
    # todo add betting round here
    game.river()
    game.print_status()
    b1 = BettingRound(game.player_chips, 0, game.big_blind, game.players_with_chips())
    b1.bet(20)
    for i in range(0, players - 1):
        b1.call_bet()
    game.betting(b1)
    game.finalise()
    game.print_status()
