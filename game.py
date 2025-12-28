# game.py
# Main game engine: setup, turns, movement, suggestions

import random
from typing import Dict, List, Optional, Tuple

from board import Board
from cards import Card, create_all_cards, ROOM_NAMES
from deck import select_solution, deal_cards
from players import Player, AIPlayer, WeaponToken, create_players
from suggestion import prompt_for_suggestion



class CluedoGame:
    def __init__(self, num_players: int = 6):
        self.board = Board()
        self.players: List[Player] = create_players(num_players)
        self.current_player_idx = 0
        self.game_over: bool = False
        self.winner: Optional["Player"] = None


        # Cards and dealing
        all_cards = create_all_cards()
        (
            self.solution_character,
            self.solution_weapon,
            self.solution_room,
            remaining_deck,
        ) = select_solution(all_cards)
        

        self.solution = (
            self.solution_character,
            self.solution_weapon,
            self.solution_room,
        )

        hands = deal_cards(remaining_deck, num_players)
        for p, hand in zip(self.players, hands):
            p.hand = hand

        for p in self.players:
            if p.is_ai:
                from cards import CHARACTER_NAMES, WEAPON_NAMES, ROOM_NAMES
                p.initialize_kb(CHARACTER_NAMES, WEAPON_NAMES, ROOM_NAMES, self.players)


        # Weapon tokens start in arbitrary rooms (can be first 6 rooms)
        self.weapons: Dict[str, WeaponToken] = {}
        for weapon_name, room in zip(  # type: ignore
            self._weapon_names(), ROOM_NAMES
        ):
            self.weapons[weapon_name] = WeaponToken(name=weapon_name, location=room)

        # For fast lookup of character -> player
        self.players_by_character = {p.character_name: p for p in self.players}
    def move_character_token_to_room(self, character_name: str, room: str):
        """Move the suggested character's token to the room."""
        if character_name not in self.players_by_character:
            return
        player = self.players_by_character[character_name]
        print(f"Moving {character_name} token from {player.position} to {room} due to suggestion.")
        player.position = room

    def move_weapon_token_to_room(self, weapon_name: str, room: str):
        """Move the suggested weapon token into the room."""
        if weapon_name not in self.weapons:
            return
        weapon = self.weapons[weapon_name]
        print(f"Moving weapon {weapon_name} from {weapon.location} to {room} due to suggestion.")
        weapon.location = room

    def _weapon_names(self):
        # Quick access without importing again
        from cards import WEAPON_NAMES

        return WEAPON_NAMES

    def show_initial_info(self):
        print("\n=== Welcome to Command-Line Cluedo (Part 1 & part 2) ===\n")
        print("Players in this game:")
        for p in self.players:
            print(f"  {p}")
        print("\nYour individual cards will NOT be shown to other players.")
        print("Each player should look at their hand when it is their turn.\n")

    def show_player_hand(self, player: Player):
        print(f"\nCards dealt to {player.character_name}:")
        for card in player.hand:
            print(f"  - {card.name} ({card.card_type.name})")
        print()

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def available_moves_for_player(self, player: Player, roll: int):
        reachable = self.board.reachable_with_steps(player.position, roll)
        return sorted(list(reachable))

    def take_turn(self, player: "Player") -> None:
        """
        One full turn for a player: they may either make an accusation
        OR move (and possibly make a suggestion).
        """
        if player.eliminated:
            print(f"\n{player.name} has been eliminated and skips their turn.")
            return

        print("\n" + "=" * 50)
        print(f"It's {player.name}'s turn.")
        print(f"Current position: {player.position}")

        # Give the player a choice: accuse or move
        while True:
            choice = input(
                "Do you want to (A)ccuse or (M)ove this turn? [M]: "
            ).strip().upper()
            if choice in ("", "M", "A"):
                break
            print("Please enter 'A' or 'M'.")
        
        if player.is_ai and player.should_accuse():
            print(f"\n{player.name} (AI) decides to make an ACCUSATION!")
            self.handle_accusation(player)
            return


        if choice == "A":
            self.handle_accusation(player)
            return

        # ----- NORMAL MOVEMENT FLOW (existing Part 1 logic) -----
        # Secret passage option first
        # ----- NORMAL MOVEMENT FLOW -----

        # Secret passage option
        if player.position in self.board.secret_passages and not self.game_over:
            use_sp = input(
                "You are in a room with a SECRET PASSAGE.\n"
                "Type 'S' to use it (no dice required) or press Enter to roll the dice: "
            ).strip().upper()
            if use_sp == "S":
                dest = self.board.destination_of_secret_passage(player.position)
                print(f"Using secret passage to {dest}.")
                player.position = dest
                self.handle_suggestion_if_in_room(player)
                return

        # Roll dice (both AI and human)
        input("\nPress Enter to roll the dice...")
        roll = self.roll_dice()
        print(f"Dice roll result: {roll}")

        # Compute reachable destinations
        possible_destinations = sorted(
            list(
                self.board.reachable_with_steps(
                    start=player.position,
                    steps=roll,
                )
            )
        )

        if not possible_destinations:
            print("No valid moves available. Turn ends.")
            return

        print("\nPossible destinations with this roll:")
        for i, room in enumerate(possible_destinations, start=1):
            print(f"  {i}. {room}")

        # --- AI chooses destination automatically ---
        if player.is_ai:
            dest = possible_destinations[0]
            print(f"AI chooses to move to: {dest}")

        # --- Human chooses manually ---
        else:
            while True:
                choice = input("Choose destination number: ").strip()
                if choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(possible_destinations):
                        dest = possible_destinations[idx - 1]
                        break
                print("Invalid choice. Try again.")

        print(f"{player.name} moved to {dest}.")
        player.position = dest
        self.handle_suggestion_if_in_room(player)     


    def handle_suggestion_if_in_room(self, player: "Player") -> None:
        """
        If the current player is in a room, force them to make a suggestion.
        Then handle refutations according to clockwise order.
        """
        from suggestion import prompt_for_suggestion  
        from cards import ROOM_NAMES  

        room = player.position
        if room not in ROOM_NAMES:
            return  # not in a room → no suggestion

        print(f"\n{player.name}, you MUST make a suggestion.")
        if player.is_ai:
            suspect, weapon, _ = player.choose_suggestion(room)
        else:
            suspect, weapon, _ = prompt_for_suggestion(player, room)


        # Move suggested character & weapon into the room 
        self.move_character_token_to_room(suspect, room)
        self.move_weapon_token_to_room(weapon, room)

        print(
            f"\nSuggestion recorded: {suspect} with the {weapon} in the {room}."
        )

        # --- NEW: handle refutation phase ---
        suggester_index = self.players.index(player)
        self.process_refutations(
            suggester_index=suggester_index,
            suspect=suspect,
            weapon=weapon,
            room=room,
        )


    def next_player_index(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def run(self):
        self.show_initial_info()
        print("Type CTRL+C at any time to quit the game.\n")

        round_counter = 1
        try:
            while not self.game_over:
                print(f"\n************ ROUND {round_counter} ************")
                player = self.players[self.current_player_idx]

                self.show_player_hand(player)
                self.take_turn(player)

                # After each turn, check if ALL players are eliminated
                if all(p.eliminated for p in self.players):
                    print("\nAll players eliminated — no one can win the game.")
                    self.game_over = True
                    break


                if self.game_over:
                    break

                self.next_player_index()
                round_counter += 1

        except KeyboardInterrupt:
            print("\n\nGame ended by user. Goodbye!")

        if self.winner:
            print(f"\nGAME OVER — Winner: {self.winner.name}")


    
    def process_refutations(
        self,
        suggester_index: int,
        suspect: str,
        weapon: str,
        room: str,
    ) -> Tuple[Optional["Player"], Optional["Card"]]:

        n = len(self.players)
        suggester = self.players[suggester_index]
        names_to_match = {suspect, weapon, room}

        # CLOCKWISE search for refuter
        for offset in range(1, n):
            idx = (suggester_index + offset) % n
            refuter = self.players[idx]

            # What cards can this refuter show?
            matching_cards = [
                card for card in refuter.hand
                if getattr(card, "name", None) in names_to_match
            ]

            if not matching_cards:
                # --- AI learns this refuter cannot have ANY of these 3 cards ---
                if suggester.is_ai:
                    suggester.record_player_cannot_have(refuter.id, suspect)
                    suggester.record_player_cannot_have(refuter.id, weapon)
                    suggester.record_player_cannot_have(refuter.id, room)

                continue

            
            print(f"\n{refuter.name} can refute the suggestion.")

            # Choose card (AI/human)
            if len(matching_cards) == 1 or refuter.is_ai:
                shown = matching_cards[0]
            else:
                print("You have the following matching cards:")
                for i, c in enumerate(matching_cards, start=1):
                    print(f"  {i}. {c.name}")
                while True:
                    choice = input("Choose a card number to show: ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(matching_cards):
                        shown = matching_cards[int(choice) - 1]
                        break
                    print("Invalid choice. Try again.")

            # Show card to suggester
            print(f"\n{refuter.name} shows a card to {suggester.name}.")
            print(f"(DEBUG / CLI) Card shown: {shown.name}")

            # --- AI KNOWLEDGE UPDATE ---
            if suggester.is_ai:
                # AI directly sees the card
                suggester.record_seen_card(shown.name)

            if refuter.is_ai:
                # AI knows it has at least one of these 3 cards
                refuter.record_player_has(refuter.id, shown.name)

            # AI learns refuter MAY have one of the suggested cards
            if suggester.is_ai:
                suggester.record_player_may_have(refuter.id, list(names_to_match))

            return refuter, shown

        # No refutation
        print("\nNo one can refute this suggestion. The suggestion stands.")
    
        # --- AI DEDUCTION: nobody has any of these 3 cards ---
        if suggester.is_ai:
            suggester.record_player_cannot_have(-1, suspect)
            suggester.record_player_cannot_have(-1, weapon)
            suggester.record_player_cannot_have(-1, room)

        return None, None


    def handle_accusation(self, player: "Player") -> None:
        """
        Allow the player to make a full accusation: (suspect, weapon, room).
        If correct → game over with winner.
        If wrong   → player is eliminated (but may still refute others).
        """
        from cards import CHARACTER_NAMES, WEAPON_NAMES, ROOM_NAMES

        print(f"\n{player.name} is making an ACCUSATION!")

        
        # AI ACCUSATION (NO INPUT)
        
        if player.is_ai:
            suspect, weapon, room = player.get_accusation()
            print(f"{player.name} (AI) accuses: {suspect} with the {weapon} in the {room}!")
        else:
            
            # HUMAN ACCUSATION (INPUT)
            

            # --- Choose suspect ---
            print("Choose a suspect:")
            for i, name in enumerate(CHARACTER_NAMES, start=1):
                print(f"  {i}. {name}")
            while True:
                c = input("Suspect number: ").strip()
                if c.isdigit() and 1 <= int(c) <= len(CHARACTER_NAMES):
                    suspect = CHARACTER_NAMES[int(c) - 1]
                    break
                print("Invalid choice. Try again.")

            # --- Choose weapon ---
            print("\nChoose a weapon:")
            for i, name in enumerate(WEAPON_NAMES, start=1):
                print(f"  {i}. {name}")
            while True:
                w = input("Weapon number: ").strip()
                if w.isdigit() and 1 <= int(w) <= len(WEAPON_NAMES):
                    weapon = WEAPON_NAMES[int(w) - 1]
                    break
                print("Invalid choice. Try again.")

            # --- Choose room ---
            print("\nChoose a room:")
            for i, name in enumerate(ROOM_NAMES, start=1):
                print(f"  {i}. {name}")
            while True:
                r = input("Room number: ").strip()
                if r.isdigit() and 1 <= int(r) <= len(ROOM_NAMES):
                    room = ROOM_NAMES[int(r) - 1]
                    break
                print("Invalid choice. Try again.")

        
        # CHECK ACCUSATION RESULT
        

        print(f"\n{player.name} accuses: {suspect} with the {weapon} in the {room}!")

        sol_char, sol_weapon, sol_room = self.solution

        if (
            suspect == sol_char.name
            and weapon == sol_weapon.name
            and room == sol_room.name
        ):
            print("\n ACCUSATION CORRECT! ")
            print(f"{player.name} WINS THE GAME!")
            self.game_over = True
            self.winner = player
        else:
            print("\n❌ ACCUSATION WRONG.")
            print(
                f"{player.name} is eliminated from making further moves/accusations "
                "but will stay in the game to refute suggestions."
            )
            player.eliminated = True
