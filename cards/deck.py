import random
from typing import List, Iterator

SUIT_MAP = {
    1: "\u2660",
    2: "\u2665",
    3: "\u2666",
    4: "\u2663"
}

NUMBER_MAP = {
    1: "A",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K"
}


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def as_text(self) -> str:
        return "S{}N{}".format(self.suit, self.number)

    def __str__(self) -> str:
        return "{} {}".format(SUIT_MAP.get(self.suit), NUMBER_MAP.get(self.number))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Card) and self.suit is o.suit and self.number is o.number

    def __hash__(self) -> int:
        return self.__str__().__hash__()


def NumberHashCard(Card):
    def __init__(card: Card):
        super.__init__(card.suit, card.number)

    def __hash__(self) -> int:
        print("this card is {}".format(self.number))
        return self.number.__hash__()


class Deck:
    def __init__(self, seed=1):
        random.seed(seed)
        self.cards = list(all_cards())
        self.card_idx = 0
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if -1 < self.card_idx < 52:
            drawn: Card = self.cards[self.card_idx]
        else:
            self.shuffle()
            drawn: Card = self.cards[self.card_idx]
        self.card_idx += 1
        return drawn

    def shuffle(self) -> List:
        self.card_idx = 0
        random.shuffle(self.cards)
        return self.cards


def all_cards() -> Iterator:
    # for each number
    for suit in range(1, 5):
        for number in range(1, 14):
            yield Card(suit, number)
