"""
Main Entry Point for Tic Tac Toe Game
Routes to Human vs Computer or Human vs Human modes
"""

import os
import random
from q_learning_agent import QLearningAgent
from human_vs_bot import HumanVsBot


def main_menu():
    """Main menu for game selection"""
    
    print("\n" + "=" * 50)
    print("TIC TAC TOE - Q-LEARNING Agent")
    print("=" * 50)
    print("\nOptions:")
    print("1. Play against Agents")
    print("2. Play Human vs Human")
    print("3. Exit")
    print("=" * 50)
    
    choice = input("Select an option (1-3): ").strip()
    
    if choice == '1':
        play_vs_bot()
    elif choice == '2':
        play_human_vs_human()
    elif choice == '3':
        print("Thank you for playing! Goodbye!")
        return False
    else:
        print("Invalid option! Please select 1, 2, or 3.")
    
    return True


def play_vs_bot():
    """Play against the trained Agent"""
    
    print("\nChoose Agent:")
    print("1. Normal model (trained against random/greedy)")
    print("2. Minimax model (trained against minimax)")
    model_choice = input("Select model (1 or 2): ").strip()
    
    if model_choice == '1':
        filename = 'q_table.csv'
        model_name = "Normal"
    elif model_choice == '2':
        filename = 'q_table_minimax.csv'
        model_name = "Minimax"
    else:
        print("Invalid choice! Defaulting to Normal model.")
        filename = 'q_table.csv'
        model_name = "Normal"
    
    if not os.path.exists(filename):
        print(f"\nERROR: Trained model not found at {filename}!")
        print("Please train the bot first.")
        return
    
    try:
        print(f"\nLoading {model_name} trained agent...")
        agent = QLearningAgent()
        agent.load_model(filename)
        
        while True:
            first_player = random.choice([1, -1])
            if first_player == 1:
                print("\nCoin toss result: Agent goes first!")
            else:
                print("\nCoin toss result: You go first!")
            
            game = HumanVsBot(agent, first_player)
            result = game.play()
            
            play_again = input("\nPlay again? (yes/no): ").strip().lower()
            if play_again not in ['yes', 'y']:
                print("\nThank you for playing!")
                break
    
    except Exception as e:
        print(f"Error during gameplay: {e}")


def play_human_vs_human():
    """Play Human vs Human"""
    
    try:
        from human_vs_human import HumanVsHuman
        
        while True:
            game = HumanVsHuman()
            result = game.play()
            
            play_again = input("\nPlay again? (yes/no): ").strip().lower()
            if play_again not in ['yes', 'y']:
                print("\nThank you for playing!")
                break
    
    except Exception as e:
        print(f"Error during gameplay: {e}")


if __name__ == "__main__":
    try:
        while main_menu():
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
