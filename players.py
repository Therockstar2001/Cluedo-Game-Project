# players.py
# Player and weapon token data

from dataclasses import dataclass, field
from typing import List
from cards import Card
from cards import CHARACTER_NAMES


@dataclass
class Player:
    id: int
    character_name: str
    position: str
    hand: List[Card] = field(default_factory=list)

    
    is_ai: bool = False  # Whether this player is an AI player
    eliminated: bool = False  # True = cannot move/suggest/accuse, but can refute
    
    @property
    def name(self):
        return self.character_name


    def __str__(self):
        status = "(ELIMINATED)" if self.eliminated else ""
        return f"Player {self.id} ({self.character_name}) at {self.position} {status}"

@dataclass
class AIPlayer(Player):

    # Knowledge Base Fields
    possible_suspects: set = field(default_factory=set)
    possible_weapons: set = field(default_factory=set)
    possible_rooms: set = field(default_factory=set)

    seen_cards: set = field(default_factory=set)

    # player_id -> set of cards they cannot possibly have
    known_not_have: dict = field(default_factory=dict)

    # player_id -> set of cards they MAY have (from refutations)
    known_may_have: dict = field(default_factory=dict)

    # player_id -> confirmed card they DO have
    known_has: dict = field(default_factory=dict)


    def initialize_kb(self, all_suspects, all_weapons, all_rooms, all_players):
        """Initialize what the AI knows at the start."""
        self.possible_suspects = set(all_suspects)
        self.possible_weapons = set(all_weapons)
        self.possible_rooms = set(all_rooms)

        # Remove AI's own cards from possible solutions
        for card in self.hand:
            if card.name in self.possible_suspects:
                self.possible_suspects.remove(card.name)
            if card.name in self.possible_weapons:
                self.possible_weapons.remove(card.name)
            if card.name in self.possible_rooms:
                self.possible_rooms.remove(card.name)

        # initialize player knowledge maps
        for p in all_players:
            self.known_not_have[p.id] = set()
            self.known_may_have[p.id] = set()
            self.known_has[p.id] = set()


    # --- Basic Recording ------------------------------------------------------

    def record_seen_card(self, card_name: str):
        """AI sees a card directly, remove from solution sets."""
        self.seen_cards.add(card_name)
        self._remove_from_possible(card_name)


    def record_player_cannot_have(self, player_id: int, card_name: str):
        """Record that a player does NOT have a given card."""
        self.known_not_have[player_id].add(card_name)

        # if that card was in MAY_HAVE for that player remove it
        self.known_may_have[player_id].discard(card_name)

        self._deduce_from_all()


    def record_player_may_have(self, player_id: int, card_list):
        """
        Record that a player refuted a suggestion and therefore
        has AT LEAST ONE of these cards.
        """
        for c in card_list:
            # They may have this card, but only if not disproven
            if c not in self.known_not_have[player_id]:
                self.known_may_have[player_id].add(c)

        self._deduce_from_all()


    def record_player_has(self, player_id: int, card_name: str):
        """If AI learns EXACTLY which card a player has."""
        self.known_has[player_id].add(card_name)
        self._remove_from_possible(card_name)

        # If the player has it, they cannot have the others
        for other in [*self.possible_suspects, *self.possible_weapons, *self.possible_rooms]:
            if other != card_name:
                self.known_not_have[player_id].add(other)

        self._deduce_from_all()


    # --- Deduction Helpers ---------------------------------------------------

    def _remove_from_possible(self, card_name):
        """Remove a card from any possible solution categories."""
        self.possible_suspects.discard(card_name)
        self.possible_weapons.discard(card_name)
        self.possible_rooms.discard(card_name)


    def _deduce_from_all(self):
        """
        This performs logical deduction based on what we know:
        - If NO PLAYER can have a card → card is in solution
        - If a card is in solution, remove it from all player possibilities
        """
        all_cards = (
            self.possible_suspects
            | self.possible_weapons
            | self.possible_rooms
        )

        for card in list(all_cards):
            # Skip cards we have seen directly
            if card in self.seen_cards:
                continue

            # If AI does not have card AND no player can have it:
            nobody_can_have = True
            for pid, cannot_set in self.known_not_have.items():
                if card not in cannot_set:
                    nobody_can_have = False
                    break

            if nobody_can_have:
                # Then card must be in the solution envelope.
                self._mark_as_solution(card)


    def _mark_as_solution(self, card):
        """Mark a card as part of the murder solution."""
        print(f"[AI DEBUG] AI infers: {card} MUST be in the solution.")

        if card in self.possible_suspects:
            self.possible_suspects = {card}

        if card in self.possible_weapons:
            self.possible_weapons = {card}

        if card in self.possible_rooms:
            self.possible_rooms = {card}


    # --- AI Decision Making ---------------------------------------------------

    def choose_suggestion(self, current_room):
        """AI chooses suggestion based on least eliminated possibilities."""
        # Pick first remaining suspect & weapon
        suspect = next(iter(self.possible_suspects))
        weapon = next(iter(self.possible_weapons))
        room = current_room
        return suspect, weapon, room


    def should_accuse(self):
        """AI accuses only when absolutely certain."""
        return (
            len(self.possible_suspects) == 1
            and len(self.possible_weapons) == 1
            and len(self.possible_rooms) == 1
        )


    def get_accusation(self):
        """Return the AI's accusation tuple."""
        return (
            next(iter(self.possible_suspects)),
            next(iter(self.possible_weapons)),
            next(iter(self.possible_rooms)),
        )


@dataclass
class WeaponToken:
    name: str
    location: str  # room name

    def __str__(self):
        return f"{self.name} in {self.location}"


def default_start_positions():
    """Map character -> starting node name"""
    mapping = {
        "Miss Scarlett": "Miss Scarlett Start",
        "Colonel Mustard": "Colonel Mustard Start",
        "Mrs. White": "Mrs. White Start",
        "Reverend Green": "Reverend Green Start",
        "Mrs. Peacock": "Mrs. Peacock Start",
        "Professor Plum": "Professor Plum Start",
    }
    return mapping

def create_players(num_players: int = 6) -> List[Player]:
    starts = default_start_positions()
    players = []

    for i in range(num_players):
        character = CHARACTER_NAMES[i]
        pos = starts[character]

        if i == num_players - 1:
            # last player = AI
            ai = AIPlayer(id=i + 1, character_name=character, position=pos, is_ai=True)
            players.append(ai)
        else:
            players.append(Player(id=i + 1, character_name=character, position=pos))

    return players

