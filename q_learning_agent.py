"""
Q-Learning Agent Module
Implements the agent that learns from games using Q-Learning
"""

import random
import csv
import os

class QLearningAgent:
    """Q-Learning agent for Tic Tac Toe
    
    Q-Table Format:
    state -> [q_val_0, q_val_1, ..., q_val_8]
    where:
    - -99 = occupied (illegal move)
    - 0  = untrained/unknown move
    """
    
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=1.0):
        """Initialize the Q-Learning agent
        
        Args:
            learning_rate: How fast the agent updates Q-values (alpha)
            discount_factor: How much future rewards matter (gamma)
            epsilon: Exploration rate (1.0 = always explore, 0.0 = always exploit)
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor 
        self.epsilon = epsilon
        self.q_table = {}
    
    def select_action(self, state, legal_moves, training=True):
        """Select an action using epsilon-greedy strategy
        
        Args:
            state: Current board state
            legal_moves: List of valid move positions
            training: If True, use epsilon-greedy. If False, use greedy (max Q-value)
        
        Returns:
            Selected move position
        """
        if training and random.random() < self.epsilon:
            return random.choice(legal_moves)
        else:
            return self.get_best_action(state, legal_moves)
    
    def get_best_action(self, state, legal_moves):
        """Get the best action for a state (highest Q-value among legal moves)"""
        if state not in self.q_table:
            return random.choice(legal_moves)
        
        q_row = self.q_table[state]
        best_value = float('-inf')
        best_moves = []
        
        for move in legal_moves:
            q_value = q_row[move]
            if q_value > best_value:
                best_value = q_value
                best_moves = [move]
            elif q_value == best_value:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(legal_moves)
    
    def get_max_q_value(self, state, legal_moves):
        """Get the maximum Q-value for a state among legal moves"""
        if not legal_moves or state not in self.q_table:
            return 0
        
        q_row = self.q_table[state]
        max_value = max([q_row[move] for move in legal_moves])
        return max_value
    
    def initialize_state(self, state, board):
        """Initialize Q-row for a new state
        
        Args:
            state: Board state (tuple)
            board: Board list [1, 0, -1, ...]
        
        Sets occupied cells to -99, empty cells to 0
        """
        if state not in self.q_table:
            q_row = []
            for cell in board:
                if cell != 0:  # Occupied (X or O)
                    q_row.append(-99)  # Illegal move
                else:
                    q_row.append(0)  # Untrained move
            self.q_table[state] = q_row
    
    def update_q_value(self, state, action, reward, next_state, next_legal_moves, board):
        """Update Q-value using Q-Learning formula:
        Q(s,a) = Q(s,a) + alpha * [r + gamma·max(Q(s',a')) - Q(s,a)]
        """
        self.initialize_state(state, board)
        
        if next_state not in self.q_table:
            next_board = list(next_state)  # Reconstruct next board
            self.initialize_state(next_state, next_board)
        
        current_q = self.q_table[state][action]
        max_next_q = self.get_max_q_value(next_state, next_legal_moves)
        
        # Only update positive rewards; negative becomes 0
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        
        # Allow negative Q-values for bad moves (losses), but keep -99 for occupied
        if self.q_table[state][action] != -99:
            self.q_table[state][action] = max(-20, min(20, new_q))  # Expanded range for heavier penalties
    
    def save_model(self, filename='q_table.csv'):
        """Save the trained Q-table to a CSV file
        
        Format:
        state,q0,q1,q2,q3,q4,q5,q6,q7,q8
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        ...
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            header = ['state'] + [f'q{i}' for i in range(9)]
            writer.writerow(header)
            
            # Write Q-values
            for state, q_row in sorted(self.q_table.items()):
                state_str = ','.join(map(str, state))
                row = [state_str] + q_row
                writer.writerow(row)
        
        print(f"Model saved to {filename}")
        print(f"Total states learned: {len(self.q_table)}")
    
    def load_model(self, filename='q_table.csv'):
        """Load a trained Q-table from a CSV file"""
        if not os.path.exists(filename):
            print(f"Model file {filename} not found.")
            return False
        
        self.q_table = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            for row in reader:
                state_str = row[0]
                q_values = [float(x) for x in row[1:]]
                
                # Reconstruct state tuple
                state = tuple(map(int, state_str.split(',')))
                self.q_table[state] = q_values
        
        print(f"Model loaded from {filename}")
        print(f"Total states loaded: {len(self.q_table)}")
        return True
    
