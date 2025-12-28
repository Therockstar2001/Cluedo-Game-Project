# Cluedo Project – Part 1  
Author: Sai Surya Sashank Dronamraju 
Course: CS670 – Artificial Intelligence  
Instructor: Arashdeep Kaur  

## 1. Project Description

This project is a command-line (CLI) implementation of the board game **Cluedo (Clue)**, focusing only on the requirements for **Project 2 – Part 1**. The objective is to simulate the structure and rules of the game using Python, including setup, movement, suggestions, and card distribution.

The game supports exactly **6 players**, each assigned one of the standard Cluedo characters. The mansion layout is implemented as a **graph**, which satisfies the project requirement of either an abstract or concrete board representation.

This Part 1 version does **not** implement refutations, accusations, or AI-based reasoning.

---

## 2. Features Implemented (Part 1 Requirements)

### ✔ Game Setup
- All 6 Cluedo characters included.
- All weapons and rooms represented.
- Board represented as a **graph** with connected rooms.
- Secret passages implemented (room-to-room teleportation without dice).
- Automatic selection of the hidden solution (Character + Weapon + Room).
- Remaining cards are shuffled and dealt evenly to players.

### ✔ Player Movement
- Dice roll determines maximum movement distance.
- Movement allowed only along valid graph edges.
- Entering a room **immediately ends movement**, as per Cluedo rules.
- Secret passages are optional and do not require a dice roll.

### ✔ Suggestions
- When a player enters a room, they must make a suggestion.
- Players choose a character and weapon; the room is automatically the one entered.
- Character token and weapon token are moved into the suggested room.

### ✔ User Interaction
- Fully text-based CLI.
- Clear prompts for rolling dice, selecting destinations, and making suggestions.
- Turn-based gameplay with all 6 players rotating in order.

---

## 3. How to Run the Game

### **Prerequisites**
- Python 3.8 or higher installed on your computer.

### **Running the Program**
1. Open the terminal in Visual Studio (VS) Code.
2. Navigate to the project folder:
   ```bash
   cd SaiSuryaSashankDronamraju_Project2_SourceCode
3. Run the game:
    python main.py
4. Follow the on-screen instructions:
    Press Enter to roll dice.
    Enter the number of your destination.
    Make suggestions when prompted.
    Press Ctrl + C at any time to quit the game.



### Cluedo Project – Part 2 (Full Game Logic + AI)
## 1. Overview

Project 2 – Part 2 expands the initial Cluedo engine by introducing complete game logic, including suggestions, refutations, accusations, player elimination, and a fully functioning AI player.
This phase transforms the Part-1 movement-based simulator into a full Cluedo gameplay loop capable of determining an actual winner (or no winner if all accuse incorrectly).

The goal is to simulate the game’s deduction mechanics while maintaining robust turn-based interactions and a clean command-line user interface.

## 2. Features Implemented (Part 2 Requirements)

## Suggestions (Enhanced)
Entering a room forces the player to make a suggestion.
Character and weapon tokens are automatically moved to the suggested room.
All other players attempt to refute by showing one matching card.
If multiple matching cards exist, the user chooses one to show.
If no player can refute, “NO PLAYER CAN REFUTE THIS SUGGESTION” is printed.

## Refutation Logic
Proper clockwise refutation checks starting from the next player.
Eliminated players can still refute, according to official Cluedo rules.
Debug/CLI log prints which card was shown for visibility.

## Supports
Single card refutation
Multiple-card refutation (choice required)
No refutation

## Accusations
Players may accuse at the start of their turn.
Accusations are checked against the hidden solution.
Correct accusation → Game ends with a winner.
Incorrect accusation → Player is eliminated from movement/accusation but can still refute.

## Player Elimination System

# Eliminated players:
Cannot move
Cannot accuse
Still refute suggestions
Game continues until:
Someone wins, or
All players are eliminated (no winner)

## Last-Player-Remaining Handling (Edge Case)
If only one active player remains, they automatically enter deduction mode.
Turn continues with movement and suggestions until a successful accusation is made.

## AI Player (Professor Plum)

# AI evaluates:
Cards seen through refutations.
Rooms already cleared.
Cards in its hand.

# Strategy includes:
Moving toward untested rooms.
Avoiding suggestions about its own known cards.
Making accusations only when logically safe.

## Stability Improvements
Invalid input detection (“Invalid choice. Try again.”)
Infinite-loop safeguards for movement.
Validation of dice destinations, room entries, and number selections.

# Graceful handling of:
Empty refutation options
Last player alive
Repeated suggestions
Out-of-range user input

## 3. Screenshots Demonstrated 

## Valid & Invalid Movement
Provided screenshots show:
A valid room entry and movement.
An invalid destination selection and error message.

## Suggestions & Refutations

# Screenshots include:
Specific card shown.
Multiple matching cards shown and user selection prompt.
AI choosing refutation.

# No Refutation Scenario
Captured when no players can refute a suggestion.

# Correct Accusation
End-of-game win screen.

# Incorrect Accusation
Player elimination message.

# Last Player Remaining
Screenshot showing only one non-eliminated player continuing the game.

# AI Logic Output
Logs show AI movement choice and deduction-based suggestion.

## 4. How to Run (Same as Part 1)

cd SaiSuryaSashankDronamraju_Project2_SourceCode
python main.py


## Follow on-screen instructions to:
Move or Accuse
Roll dice
Make suggestions
Provide refutations
Attempt accusations

## 5. Additional Details (Development Notes)
Language: Python 3.8+
Architecture: Object-oriented (Players, Deck, Board, Suggestions, Game Engine)
Board: Implemented as a graph (adjacency list) for room connections.
AI: Rule-based deduction system using incremental knowledge filtering.
Testing: Verified through exhaustive screenshot cases and multiple full-game runs.
Focus: Game stability, correctness, and exact adherence to project specifications.

## 6. Conclusion

Part 2 completes the Cluedo simulation by integrating all essential gameplay rules—suggestions, refutations, accusations, and elimination. The addition of a strategic AI makes the game dynamic and unpredictable, while robust handling of edge cases ensures reliable gameplay. With full movement, deduction, and end-game logic, the program now functions as a comprehensive command-line version of Cluedo, faithfully meeting all project requirements.