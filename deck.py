# deck.py
# Deck handling: solution selection and dealing

import random
from typing import List, Tuple
from cards import Card, CardType, create_all_cards


def select_solution(all_cards: List[Card]) -> Tuple[Card, Card, Card, List[Card]]:
    """Pick one Character, one Weapon, one Room as solution, return rest as deck."""
    characters = [c for c in all_cards if c.card_type == CardType.CHARACTER]
    weapons = [c for c in all_cards if c.card_type == CardType.WEAPON]
    rooms = [c for c in all_cards if c.card_type == CardType.ROOM]

    solution_character = random.choice(characters)
    solution_weapon = random.choice(weapons)
    solution_room = random.choice(rooms)

    solution_set = {solution_character, solution_weapon, solution_room}
    remaining = [c for c in all_cards if c not in solution_set]
    random.shuffle(remaining)
    return solution_character, solution_weapon, solution_room, remaining


def deal_cards(deck: List[Card], num_players: int) -> List[List[Card]]:
    """Deal remaining deck evenly among players."""
    hands = [[] for _ in range(num_players)]
    i = 0
    while deck:
        hands[i % num_players].append(deck.pop())
        i += 1
    return hands
