"""
Training Module for Q-Learning Agent
Trains the agent through self-play games
"""

import random
from tic_tac_toe import TicTacToe
from q_learning_agent import QLearningAgent


def minimax_move(game, player):
    """Find the minimax-optimal move for the given player."""
    def minimax(game_instance, current_player):
        if game_instance.is_game_over():
            winner = game_instance.check_winner()
            if winner == 1:
                return 20
            if winner == -1:
                return -20
            return 0

        legal = game_instance.get_legal_moves()
        if current_player == 1:
            best_score = -float('inf')
            for move in legal:
                game_instance.make_move(move, 1)
                score = minimax(game_instance, -1)
                game_instance.board[move] = 0
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in legal:
                game_instance.make_move(move, -1)
                score = minimax(game_instance, 1)
                game_instance.board[move] = 0
                best_score = min(best_score, score)
            return best_score

    opponent_moves = []
    best_score = float('inf') if player == -1 else -float('inf')
    for move in game.get_legal_moves():
        game.make_move(move, player)
        score = minimax(game, -player)
        game.board[move] = 0

        if player == 1:
            if score > best_score:
                best_score = score
                opponent_moves = [move]
            elif score == best_score:
                opponent_moves.append(move)
        else:
            if score < best_score:
                best_score = score
                opponent_moves = [move]
            elif score == best_score:
                opponent_moves.append(move)

    return random.choice(opponent_moves)


def train_agent(num_games=200000, initial_epsilon=1.0, final_epsilon=0.01, opponent_type='model', opponent_random_rate=0.3):
    """Train the Q-Learning agent through self-play.

    Args:
        num_games: Number of training games.
        initial_epsilon: Starting exploration rate.
        final_epsilon: Final exploration rate.
        opponent_type: 'model' for the existing model-style opponent, 'minimax' for a minimax opponent.
        opponent_random_rate: Probability that the model opponent chooses a random move.

    Returns:
        Trained agent, training results dictionary.
    """
    if opponent_type not in {'model', 'minimax'}:
        raise ValueError("opponent_type must be 'model' or 'minimax'")

    agent = QLearningAgent(learning_rate=0.1, discount_factor=0.9, epsilon=initial_epsilon)
    game = TicTacToe()
    results = {'ai_wins': 0, 'opponent_wins': 0, 'draws': 0}
    epsilon_decay = (initial_epsilon - final_epsilon) / num_games
    progress_interval = max(1, num_games // 100)

    print(f"Training agent for {num_games} games...")
    print(f"Opponent type: {opponent_type}")
    print(f"Epsilon decays from {initial_epsilon} to {final_epsilon}")
    print(f"Learning rate: {agent.learning_rate}, Discount factor: {agent.discount_factor}\n")

    for game_num in range(1, num_games + 1):
        game.reset()
        move_history = []
        is_agent_turn = random.choice([True, False])

        while not game.is_game_over():
            state = game.board_to_state()
            legal_moves = game.get_legal_moves()
            agent.initialize_state(state, game.board)

            if is_agent_turn:
                action = agent.select_action(state, legal_moves, training=True)
                game.make_move(action, 1)
                move_history.append((state, action, 1))
            else:
                if opponent_type == 'model':
                    if random.random() < opponent_random_rate:
                        action = random.choice(legal_moves)
                    else:
                        action = agent.select_action(state, legal_moves, training=False)
                else:
                    action = minimax_move(game, -1)

                game.make_move(action, -1)
                move_history.append((state, action, -1))

            is_agent_turn = not is_agent_turn

        winner = game.check_winner()
      
        win_reward = 10
        loss_reward = -20
        draw_reward = 5

        if winner == 1:
            reward = win_reward
            results['ai_wins'] += 1
        elif winner == -1:
            reward = loss_reward
            results['opponent_wins'] += 1
        else:
            reward = draw_reward
            results['draws'] += 1

        for i in range(len(move_history)):
            state, action, player = move_history[i]
            if player == 1:
                if i + 2 < len(move_history):
                    next_state, _, _ = move_history[i + 2]
                    next_legal_moves = [idx for idx, val in enumerate(next_state) if val == 0]
                    agent.update_q_value(state, action, 0, next_state, next_legal_moves, state)
                else:
                    agent.update_q_value(state, action, reward, game.board_to_state(), [], state)

        agent.epsilon = max(final_epsilon, initial_epsilon - epsilon_decay * game_num)

        if game_num % progress_interval == 0 or game_num == num_games:
            win_pct = 100 * results['ai_wins'] / game_num
            loss_pct = 100 * results['opponent_wins'] / game_num
            draw_pct = 100 * results['draws'] / game_num
            average_reward = (results['ai_wins']*10 + results['draws']*5 + results['opponent_wins']*-20) / game_num

            print(f"Game {game_num}/{num_games} | Epsilon: {agent.epsilon:.4f} | Wins: {results['ai_wins']} ({win_pct:.1f}%) | "
                  f"Losses: {results['opponent_wins']} ({loss_pct:.1f}%) | Draws: {results['draws']} ({draw_pct:.1f}%)")
            print(f"  Q-table size: {len(agent.q_table)} | Avg reward/game: {average_reward:.3f}\n")

    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print(f"Final Results:")
    print(f"  AI Wins: {results['ai_wins']} ({100*results['ai_wins']/num_games:.1f}%)")
    print(f"  Losses: {results['opponent_wins']} ({100*results['opponent_wins']/num_games:.1f}%)")
    print(f"  Draws: {results['draws']} ({100*results['draws']/num_games:.1f}%)")
    print(f"  Average reward per game: {(results['ai_wins']*10 + results['draws']*5) / num_games:.2f}")
    print(f"  Total states learned: {len(agent.q_table)}")
    print("="*50 + "\n")

    return agent, results


if __name__ == "__main__":
    print("\n" + "="*50)
    print("TIC TAC TOE TRAINING MODULE")
    print("="*50)
    opponent_choice = input("Choose opponent type:\n 1) Model opponent\n 2) Minimax opponent\nSelect 1 or 2: ").strip()
    opponent_type = 'model' if opponent_choice == '1' else 'minimax'
    num_games_input = input("Number of training games [200000]: ").strip()
    num_games = int(num_games_input) if num_games_input.isdigit() else 200000
    agent, results = train_agent(num_games=num_games, initial_epsilon=1.0, final_epsilon=0.01, opponent_type=opponent_type)
    filename = 'q_table_minimax.csv' if opponent_type == 'minimax' else 'q_table.csv'
    agent.save_model(filename)
    print(f"Model saved to {filename}! Ready to play.")
