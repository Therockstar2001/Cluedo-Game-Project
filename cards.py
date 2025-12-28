# cards.py
# Card definitions for Cluedo project (Characters, Weapons, Rooms)

from enum import Enum, auto
from dataclasses import dataclass


class CardType(Enum):
    CHARACTER = auto()
    WEAPON = auto()
    ROOM = auto()


@dataclass(frozen=True)
class Card:
    name: str
    card_type: CardType


CHARACTER_NAMES = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Reverend Green",
    "Mrs. Peacock",
    "Professor Plum",
]

WEAPON_NAMES = [
    "Candlestick",
    "Dagger",
    "Lead Pipe",
    "Revolver",
    "Rope",
    "Wrench",
]

ROOM_NAMES = [
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Dining Room",
    "Billiard Room",
    "Library",
    "Lounge",
    "Hall",
    "Study",
]


def create_all_cards():
    """Return a list of all 6 + 6 + 9 cards."""
    cards = []
    for n in CHARACTER_NAMES:
        cards.append(Card(n, CardType.CHARACTER))
    for n in WEAPON_NAMES:
        cards.append(Card(n, CardType.WEAPON))
    for n in ROOM_NAMES:
        cards.append(Card(n, CardType.ROOM))
    return cards
