# board.py
# Graph-based mansion layout and secret passages

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class Board:
    """Graph of positions (rooms + starting spots)."""

    adjacency: Dict[str, List[str]] = field(default_factory=dict)
    secret_passages: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self._init_rooms()
        self._init_secret_passages()
        self._init_start_positions()

    def _add_edge(self, a: str, b: str):
        self.adjacency.setdefault(a, []).append(b)
        self.adjacency.setdefault(b, []).append(a)

    def _init_rooms(self):
        # Rooms from classic Cluedo, adjacencies approximated as a graph.
        rooms = [
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
        for r in rooms:
            self.adjacency.setdefault(r, [])

        self._add_edge("Kitchen", "Ballroom")
        self._add_edge("Kitchen", "Dining Room")
        self._add_edge("Ballroom", "Conservatory")
        self._add_edge("Ballroom", "Hall")
        self._add_edge("Ballroom", "Dining Room")
        self._add_edge("Conservatory", "Billiard Room")
        self._add_edge("Dining Room", "Hall")
        self._add_edge("Dining Room", "Lounge")
        self._add_edge("Billiard Room", "Library")
        self._add_edge("Billiard Room", "Hall")
        self._add_edge("Library", "Hall")
        self._add_edge("Library", "Study")
        self._add_edge("Lounge", "Hall")
        self._add_edge("Hall", "Study")

    def _init_secret_passages(self):
        # Secret passages do NOT require a dice roll.
        self.secret_passages = {
            "Kitchen": "Study",
            "Study": "Kitchen",
            "Conservatory": "Lounge",
            "Lounge": "Conservatory",
        }

    def _init_start_positions(self):
        # Starting hallway-like nodes for each character.
        starts = {
            "Miss Scarlett Start": "Lounge",
            "Colonel Mustard Start": "Dining Room",
            "Mrs. White Start": "Kitchen",
            "Reverend Green Start": "Ballroom",
            "Mrs. Peacock Start": "Conservatory",
            "Professor Plum Start": "Study",
        }
        for start, room in starts.items():
            self._add_edge(start, room)

    def neighbors(self, position: str) -> List[str]:
        return self.adjacency.get(position, [])

    def reachable_with_steps(self, start: str, steps: int) -> Set[str]:
        """Return all positions reachable with <= steps along edges."""
        from collections import deque

        visited = {start: 0}
        q = deque([start])

        while q:
            current = q.popleft()
            current_dist = visited[current]
            if current_dist == steps:
                continue
            for nb in self.neighbors(current):
                if nb not in visited or visited[nb] > current_dist + 1:
                    visited[nb] = current_dist + 1
                    q.append(nb)

        return {pos for pos, dist in visited.items() if dist <= steps and pos != start}

    def has_secret_passage(self, room: str) -> bool:
        return room in self.secret_passages

    def destination_of_secret_passage(self, room: str) -> str:
        return self.secret_passages[room]
