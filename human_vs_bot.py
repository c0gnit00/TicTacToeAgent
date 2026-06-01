"""
Human vs Computer Game Mode
Allows a human player to play against the trained AI bot
"""

import random
from tic_tac_toe import TicTacToe
from q_learning_agent import QLearningAgent


class HumanVsBot:
    """Human vs Bot game mode"""
    
    def __init__(self, agent, first_player=1):
        """Initialize game with trained agent
        
        Args:
            agent: Trained QLearningAgent instance
            first_player: 1 for AI first (X), -1 for human first (O)
        """
        self.agent = agent
        self.game = TicTacToe()
        self.first_player = first_player
    
    def play(self):
        """Play a game of Human vs Bot
        
        Returns:
            'ai' if AI wins
            'human' if human wins
            'draw' if game is a draw
        """
        print("\n" + "="*50)
        print("HUMAN vs COMPUTER")
        print("="*50)
        if self.first_player == 1:
            print("Computer plays as X (goes first)")
            print("You play as O\n")
        else:
            print("You play as X (go first)")
            print("Computer plays as O\n")
        
        self.game.reset()
        
        current_player = self.first_player
        
        while not self.game.is_game_over():
            self.game.display_board()
            
            if current_player == 1:
                # AI's turn
                state = self.game.board_to_state()
                legal_moves = self.game.get_legal_moves()
                
                # Use trained Q-table (no exploration, only exploitation)
                action = self.agent.select_action(state, legal_moves, training=False)
                
                print(f"\nComputer chooses position {action}")
                self.game.make_move(action, 1)
                
            else:
                # Human's turn
                while True:
                    try:
                        position = int(input("\nEnter your move (0-8): "))
                        if self.game.is_valid_move(position):
                            self.game.make_move(position, -1)
                            break
                        else:
                            print("Invalid move! Position already taken or out of range.")
                    except ValueError:
                        print("Invalid input! Enter a number between 0-8.")
            
            # Check for winner
            winner = self.game.check_winner()
            if winner == 1:
                self.game.display_board()
                print("\n" + "="*50)
                print("COMPUTER WINS! Better luck next time!")
                print("="*50)
                return 'ai'
            elif winner == -1:
                self.game.display_board()
                print("\n" + "="*50)
                print("YOU WIN! Congratulations!")
                print("="*50)
                return 'human'
            
            # Check for draw
            if self.game.is_draw():
                self.game.display_board()
                print("\n" + "="*50)
                print("IT'S A DRAW!")
                print("="*50)
                return 'draw'
            
            current_player = -1 if current_player == 1 else 1


def play_human_vs_bot():
    """Main function to run Human vs Bot mode"""
    print("Loading trained agent...")
    agent = QLearningAgent()
    
    if not agent.load_model('q_table.csv'):
        print("ERROR: Could not load trained model.")
        print("Please run train_agent.py first to train the bot.")
        return
    
    print()
    
    while True:
        first_player = random.choice([1, -1])
        if first_player == 1:
            print("\nCoin toss result: Computer goes first!")
        else:
            print("\nCoin toss result: You go first!")

        game = HumanVsBot(agent, first_player)
        result = game.play()

        # Ask if player wants to play again
        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\nThank you for playing! Goodbye!")
            break


if __name__ == "__main__":
    play_human_vs_bot()
