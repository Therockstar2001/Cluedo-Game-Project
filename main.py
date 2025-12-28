# main.py
# Entry point for the Cluedo game (Part 1 & Part 2 with one AI player)

from game import CluedoGame

def main():
    game = CluedoGame(num_players=6)

    # Make the LAST player an AI agent
    # (Professor Plum becomes AI)
    ai_player = game.players[-1]
    ai_player.is_ai = True

    print(f"\nAI Player Assigned: {ai_player.character_name}\n")

    game.run()

if __name__ == "__main__":
    main()
