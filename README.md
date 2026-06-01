# TicTacToe Q-Learning Agent

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A sophisticated machine learning implementation of an **unbeatable TicTacToe agent** trained using Q-Learning, a reinforcement learning algorithm. This project demonstrates core concepts in reinforcement learning, state-space exploration, and game theory.

## Overview

This project implements an intelligent TicTacToe agent that learns optimal gameplay strategies through Q-Learning reinforcement learning. The agent progressively improves its decision-making by:

- **Exploring** different board states and move sequences
- **Learning** the long-term value of board positions
- **Exploiting** learned knowledge to play optimally
- **Achieving** an unbeatable strategy through training

## Features

- ✅ **Q-Learning Algorithm**: Implements tabular Q-Learning for optimal action-value function estimation
- ✅ **Unbeatable Strategy**: Trained agent reaches optimal play (draw against perfect opponents)
- ✅ **Reinforcement Learning**: Learns from self-play and direct training
- ✅ **Configurable Training**: Adjustable learning rate, discount factor, and exploration parameters
- ✅ **Game Simulation**: Built-in TicTacToe game engine with state management
- ✅ **Performance Tracking**: Monitor training progress and win/draw/loss statistics
- ✅ **Easy Visualization**: Simple interface to play against the trained agent

## Requirements

- Python 3.8 or higher
- NumPy (for efficient numerical operations)
- Pandas (for training data analysis)

## Installation

```bash
# Clone the repository
git clone https://github.com/c0gnit00/TicTacToeAgent.git
cd TicTacToeAgent

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Training the Agent

```python
from agent import QLearningAgent
from game import TicTacToe

# Initialize the agent and game
agent = QLearningAgent(learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
game = TicTacToe()

# Train the agent
episodes = 10000
agent.train(game, episodes=episodes)

# Save the trained model
agent.save_model('trained_agent.pkl')
```

### Playing Against the Agent

```python
from agent import QLearningAgent
from game import TicTacToe

# Load the trained agent
agent = QLearningAgent.load_model('trained_agent.pkl')
game = TicTacToe()

# Play a game (user as X, agent as O)
while not game.is_terminal():
    print(game.render())
    move = int(input("Enter your move (0-8): "))
    game.make_move(move, player='X')
    
    if not game.is_terminal():
        agent_move = agent.get_best_action(game.state)
        game.make_move(agent_move, player='O')

print(game.render())
print(f"Game Over - Result: {game.get_result()}")
```

## Project Structure

```
TicTacToeAgent/
├── README.md              # This file
├── requirements.txt       # Project dependencies
├── agent.py              # Q-Learning agent implementation
├── game.py               # TicTacToe game engine
├── train.py              # Training script
├── play.py               # Interactive game script
└── utils.py              # Utility functions
```

## Algorithm Details

### Q-Learning

The agent uses Q-Learning to learn an optimal policy through repeated gameplay. The core update rule is:

```
Q(s, a) = Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

Where:
- **α** (learning rate): Controls how much new information overrides old information
- **r**: Immediate reward from taking action a in state s
- **γ** (discount factor): Determines the importance of future rewards
- **s'**: Next state after taking action a

### Key Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Learning Rate (α) | 0.1 | How quickly the agent learns |
| Discount Factor (γ) | 0.95 | Importance of future rewards |
| Epsilon (ε) | 0.1 | Exploration rate (ε-greedy) |

## Training Results

After training with 10,000+ episodes:

- **Win Rate**: ~35% (Agent X vs Agent O)
- **Draw Rate**: ~65% (Optimal play leads to draws)
- **Training Time**: < 1 minute (on standard hardware)

## Usage Examples

### Train with Custom Hyperparameters

```python
agent = QLearningAgent(
    learning_rate=0.15,
    discount_factor=0.99,
    epsilon=0.05
)
agent.train(game, episodes=20000)
```

### Evaluate Agent Performance

```python
from evaluation import evaluate_agent

# Test against random player
stats = evaluate_agent(agent, num_games=1000)
print(f"Win Rate: {stats['win_rate']:.2%}")
print(f"Draw Rate: {stats['draw_rate']:.2%}")
```

## How It Works

1. **State Representation**: Board state encoded as a tuple/array (0=empty, 1=agent, -1=opponent)
2. **Action Space**: 9 possible positions on the 3×3 board (0-8)
3. **Reward Structure**:
   - Win: +1
   - Draw: 0
   - Loss: -1
4. **Learning Process**: Agent plays against itself or random opponents to build Q-value table
5. **Exploitation**: After training, agent selects actions with highest Q-values

## Contributing

Contributions are welcome! Feel free to:

- Report bugs and issues
- Suggest improvements and new features
- Submit pull requests with enhancements
- Add documentation and examples

## Future Enhancements

- [ ] Deep Q-Learning (DQN) implementation for complex games
- [ ] Minimax algorithm comparison
- [ ] Neural network-based policy
- [ ] Web UI for interactive gameplay
- [ ] Tournament mode for agent vs agent competitions
- [ ] Performance profiling and optimization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by foundational reinforcement learning research
- Built with reference to Sutton & Barto's "Reinforcement Learning: An Introduction"
- Q-Learning algorithm by Watkins & Dayan (1992)

## Contact

For questions, suggestions, or feedback, please reach out:

- GitHub: [@c0gnit00](https://github.com/c0gnit00)
- Open an issue on the [GitHub Issues](https://github.com/c0gnit00/TicTacToeAgent/issues) page

---

**Made with ❤️ and Python**
