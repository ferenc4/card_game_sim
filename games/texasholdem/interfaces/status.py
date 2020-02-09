from abc import ABC
from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple

from cards.deck import NUMBER_MAP, SUIT_MAP


class GameStatusComponent:
    def column(self) -> str:
        raise NotImplementedError

    def value(self) -> str:
        raise NotImplementedError


@dataclass
class BoolStatus(GameStatusComponent, ABC):
    player: int
    value: bool

    def value(self) -> str:
        return str(super().value)


@dataclass
class ChipStatus(GameStatusComponent):
    player: int
    chip_count: int

    def column(self) -> str:
        return "p{}ChipCount".format(self.player)

    def value(self) -> str:
        return str(self.chip_count)


@dataclass
class CheckedStatus(BoolStatus):
    def column(self) -> str:
        return "p{}Checked".format(super().player)


class FoldedStatus(BoolStatus):
    def column(self) -> str:
        return "p{}Folded".format(super().player)


class CardPositionIdentifier(NamedTuple):
    player: int
    card_index: int


@dataclass
class CardSuitStatus(GameStatusComponent):
    cpi: CardPositionIdentifier
    suit: int

    def column(self) -> str:
        return "p{}Card{}Suit".format(self.cpi.player, self.cpi.card_index)

    def value(self) -> str:
        return SUIT_MAP.get(self.suit)


@dataclass
class CardNumberStatus(GameStatusComponent):
    cpi: CardPositionIdentifier
    number: int

    def column(self) -> str:
        return "p{}Card{}Number".format(self.cpi.player, self.cpi.card_index)

    def value(self) -> str:
        return NUMBER_MAP.get(self.number)


@dataclass
class GameStatus:
    current_player: int
    chips: [ChipStatus]
    checked: [CheckedStatus]
    folded: [FoldedStatus]
    hand_suits: [CardSuitStatus]
    hand_numbers: [CardNumberStatus]


class GameInput(NamedTuple):
    action: str
    amount: int
