"""
Human vs Human Game Mode
Allows two human players to play against each other
"""

import random
from tic_tac_toe import TicTacToe


class HumanVsHuman:
    """Human vs Human game mode"""
    
    def __init__(self):
        """Initialize game"""
        self.game = TicTacToe()
        self.player1_name = ""
        self.player2_name = ""
    
    def play(self):
        """Play a game of Human vs Human
        
        Returns:
            Player name who won, or 'draw' if it's a draw
        """
        print("\n" + "="*50)
        print("HUMAN vs HUMAN")
        print("="*50)
        
        # Get player names
        self.player1_name = input("Enter Player 1 name: ").strip()
        if not self.player1_name:
            self.player1_name = "Player 1"
        
        self.player2_name = input("Enter Player 2 name: ").strip()
        if not self.player2_name:
            self.player2_name = "Player 2"
        
        print(f"\n{self.player1_name} plays as X")
        print(f"{self.player2_name} plays as O\n")
        
        # Coin toss to decide who goes first
        print("Running coin toss to decide who goes first...")
        toss_result = random.randint(0, 1)
        if toss_result == 0:
            print(f"Result: {self.player1_name} goes first!\n")
            current_player = 1
        else:
            print(f"Result: {self.player2_name} goes first!\n")
            current_player = -1
        
        self.game.reset()
        
        while not self.game.is_game_over():
            self.game.display_board()
            
            if current_player == 1:
                player_name = self.player1_name
                symbol = 'X'
            else:
                player_name = self.player2_name
                symbol = 'O'
            
            # Get player's move
            while True:
                try:
                    position = int(input(f"\n{player_name} ({symbol}), enter your move (0-8): "))
                    if self.game.is_valid_move(position):
                        self.game.make_move(position, current_player)
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
                print(f"{self.player1_name} WIN! Congratulations!")
                print("="*50)
                return self.player1_name
            elif winner == -1:
                self.game.display_board()
                print("\n" + "="*50)
                print(f"{self.player2_name} WIN! Congratulations!")
                print("="*50)
                return self.player2_name
            
            # Check for draw
            if self.game.is_draw():
                self.game.display_board()
                print("\n" + "="*50)
                print("IT'S A DRAW!")
                print("="*50)
                return 'draw'
            
            # Switch player
            current_player = -1 if current_player == 1 else 1


def play_human_vs_human():
    """Main function to run Human vs Human mode"""
    
    while True:
        game = HumanVsHuman()
        result = game.play()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\nThank you for playing! Goodbye!")
            break


if __name__ == "__main__":
    play_human_vs_human()
