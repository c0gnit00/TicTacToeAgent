"""
TicTacToe Game Logic Module
Handles board representation, move validation, and win checking
"""

class TicTacToe:
    """Game logic for Tic Tac Toe
    
    Board representation:
    - Positions 0-8 (0-2: top row, 3-5: middle row, 6-8: bottom row)
    - 1 = AI (X)
    - -1 = Human (O)
    - 0 = Empty
    """
    
    def __init__(self):
        # Board: 1 = AI (X), -1 = Human (O), 0 = Empty
        self.board = [0] * 9
    
    def reset(self):
        """Reset the board for a new game"""
        self.board = [0] * 9
    
    def display_board(self):
        """Display the board in console format"""
        print("\nCurrent Board:")
        symbols = {1: 'X', -1: 'O', 0: ' '}
        for i in range(3):
            row = []
            for j in range(3):
                idx = i * 3 + j
                row.append(symbols[self.board[idx]])
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i < 2:
                print("-----------")
        print("\nPositions (0-8):")
        print(" 0 | 1 | 2 ")
        print("-----------")
        print(" 3 | 4 | 5 ")
        print("-----------")
        print(" 6 | 7 | 8 ")
    
    def get_legal_moves(self):
        """Return list of empty positions"""
        return [i for i in range(9) if self.board[i] == 0]
    
    def is_valid_move(self, position):
        """Check if a move is valid"""
        return 0 <= position < 9 and self.board[position] == 0
    
    def make_move(self, position, player):
        """Make a move on the board
        
        Args:
            position: Move position (0-8)
            player: 1 for AI (X), -1 for Human (O)
        
        Returns:
            True if move was successful, False otherwise
        """
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False
    
    def check_winner(self):
        """Check if someone has won
        
        Returns:
            1 if AI (X) wins
            -1 if Human (O) wins
            0 if no winner yet
        """
        # Winning combinations
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combos:
            values = [self.board[i] for i in combo]
            if values[0] == values[1] == values[2] != 0:
                return values[0]
        
        return 0
    
    def is_draw(self):
        """Check if the game is a draw"""
        return len(self.get_legal_moves()) == 0 and self.check_winner() == 0
    
    def is_game_over(self):
        """Check if the game has ended"""
        return self.check_winner() != 0 or self.is_draw()
    
    def board_to_state(self):
        """Convert board to a hashable tuple for Q-table indexing"""
        return tuple(self.board)
    
    def board_to_string(self):
        """Convert board to string for CSV/TXT storage"""
        return ','.join(map(str, self.board))
    
    @staticmethod
    def string_to_board(board_string):
        """Convert string from CSV back to board list"""
        return [int(x) for x in board_string.split(',')]
