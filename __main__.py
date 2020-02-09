from cards.deck import RandomDeck
from games.texasholdem.interfaces.console import ConsoleInterface
from games.texasholdem.interfaces.status import CardPositionIdentifier, CardNumberStatus

__author__ = "Ferenc Fazekas"

from games.texasholdem.texasholdem import TexasHoldem


def distribution_check():
    counts = dict()
    for i in range(0, 100000):
        deck = RandomDeck()
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
    game = TexasHoldem(ConsoleInterface(), players)
    game.deal_hands()
    game.flop()
    game.turn()
    game.river()
    game.print_status()
    game.conduct_betting_round()
    game.finalise()
    game.print_status()


if __name__ == "__main__":
    main()
    # status = CardNumberStatus(CardPositionIdentifier(1, 2), 14)
    # print(status)
