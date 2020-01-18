from cards.deck import Deck
from games.texasholdem.texasholdem import TexasHoldem, BettingRound


def distribution_check():
    counts = dict()
    for i in range(0, 100000):
        deck = Deck()
        for card_idx in range(0, 10):
            drawn = deck.draw()
            if counts.get(drawn):
                counts[drawn] += 1
            else:
                counts[drawn] = 1
        deck.shuffle()

    print("Counts of {} items.".format(counts.keys().__len__()))
    for key, val in counts.items():
        print("{}:\t{}".format(key, val))


def main():
    players = 8
    game = TexasHoldem(players)
    game.deal_hands()
    game.flop()
    game.turn()
    game.river()
    game.print_status()
    b1 = BettingRound(game.player_chips, 0, game.big_blind, game.players_with_chips())
    b1.bet(20)
    for i in range(0, players - 1):
        b1.call_bet()
    game.betting(b1)
    game.finalise()
    game.print_status()


main()
