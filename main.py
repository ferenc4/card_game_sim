from cards.deck import Deck
from games.texasholdem import TexasHoldem


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
    game = TexasHoldem(5)
    game.deal_hands()

    game.flop()
    game.turn()
    game.river()
    game.status()


main()
