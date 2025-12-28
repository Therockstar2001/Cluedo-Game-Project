# suggestion.py
# Suggestion handling for Part 1 

from typing import Dict, Tuple
from players import Player, WeaponToken
from cards import CHARACTER_NAMES, WEAPON_NAMES



def prompt_for_suggestion(player, room: str):
    """
    Ask the player which suspect and weapon they want to suggest.
    """
    print(f"You are in the room: {room}")

    from cards import CHARACTER_NAMES, WEAPON_NAMES

    # Choose suspect
    print("\nAvailable Characters:")
    for i, c in enumerate(CHARACTER_NAMES, start=1):
        print(f"  {i}. {c}")
    while True:
        choice = input("Choose a character number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CHARACTER_NAMES):
            suspect = CHARACTER_NAMES[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    # Choose weapon
    print("\nAvailable Weapons:")
    for i, w in enumerate(WEAPON_NAMES, start=1):
        print(f"  {i}. {w}")
    while True:
        choice = input("Choose a weapon number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(WEAPON_NAMES):
            weapon = WEAPON_NAMES[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    return suspect, weapon, room



def move_tokens_for_suggestion(
    players_by_character: Dict[str, Player],
    weapons_by_name: Dict[str, WeaponToken],
    suggested_character: str,
    suggested_weapon: str,
    room: str,
):
    """Move character and weapon tokens into the suggestion room."""
    # Character movement
    char_player = players_by_character.get(suggested_character)
    if char_player:
        print(
            f"Moving {suggested_character} token from "
            f"{char_player.position} to {room} due to suggestion."
        )
        char_player.position = room

    # Weapon movement
    weapon_token = weapons_by_name.get(suggested_weapon)
    if weapon_token:
        print(
            f"Moving weapon {suggested_weapon} from "
            f"{weapon_token.location} to {room} due to suggestion."
        )
        weapon_token.location = room
