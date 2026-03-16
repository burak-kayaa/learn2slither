# learn2slither

A reinforcement learning project where a snake agent learns to play a Snake game autonomously using **Q-learning**. The agent receives no hard-coded strategy — it discovers how to navigate the board, eat green apples, avoid red apples, walls, and its own body entirely through trial and error.

Built as a [42 School](https://42.fr) project.

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
  - [Environment](#environment)
  - [State Representation](#state-representation)
  - [Action Space](#action-space)
  - [Reward System](#reward-system)
  - [Q-Learning Algorithm](#q-learning-algorithm)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Training a New Model](#training-a-new-model)
  - [Evaluating a Trained Model](#evaluating-a-trained-model)
  - [Graphical User Interface](#graphical-user-interface)
  - [CLI Reference](#cli-reference)
  - [Makefile Targets](#makefile-targets)
- [Configuration](#configuration)
- [Pre-trained Models](#pre-trained-models)
- [Testing](#testing)
- [Architecture](#architecture)
  - [Training Loop](#training-loop)
  - [Key Design Decisions](#key-design-decisions)

## Overview

The game takes place on a **10x10 grid** where:

- The **snake** starts with a length of 3 and moves in one of four cardinal directions each step.
- **Green apples** (2 on the board) increase the snake's length by 1 when eaten.
- **Red apples** (1 on the board) decrease the snake's length by 1 when eaten.
- The game ends when the snake hits a **wall**, collides with **itself**, or shrinks to **zero length**.

The agent uses a Q-table to map perceived states to action values, learning optimal behavior over thousands of episodes.

## How It Works

### Environment

The environment is a bounded 10x10 grid. Each cell can be empty, occupied by the snake's body, or contain an apple. The board is surrounded by implicit walls — moving outside the grid boundaries results in a wall collision and game over.

```
Board layout (10x10):

  W W W W W W W W W W W W
  W 0 0 0 0 0 0 0 0 0 0 W
  W 0 0 0 G 0 0 0 0 0 0 W
  W 0 0 0 0 0 0 0 0 0 0 W
  W 0 0 0 S S S 0 0 0 0 W    S = Snake, G = Green Apple
  W 0 0 0 0 0 0 0 R 0 0 W    R = Red Apple, W = Wall
  W 0 0 0 0 G 0 0 0 0 0 W    0 = Empty
  W 0 0 0 0 0 0 0 0 0 0 W
  W 0 0 0 0 0 0 0 0 0 0 W
  W 0 0 0 0 0 0 0 0 0 0 W
  W 0 0 0 0 0 0 0 0 0 0 W
  W W W W W W W W W W W W
```

### State Representation

The agent perceives the world through a **ray-casting vision system**. From the snake's head, rays are cast in four cardinal directions. Each ray reports:

1. **Object type**: the first non-empty entity encountered (`WALL`, `SNAKE`, `GREEN_APPLE`, `RED_APPLE`)
2. **Distance bucket**: how far away it is (`CLOSE` = 1 cell, `NEAR` = 2-3 cells, `FAR` = 4+ cells)

The raw vision is then converted into a **rotation-invariant** encoding relative to the snake's current facing direction. This produces a **6-element tuple**:

```
(ahead_object, ahead_distance, left_object, left_distance, right_object, right_distance)
```

The backward direction is excluded since the snake cannot reverse into itself.

This rotation-invariant encoding means the agent learns direction-agnostic patterns (e.g., "a wall is CLOSE ahead" is the same state regardless of whether the snake faces north, south, east, or west), dramatically reducing the state space.

### Action Space

Instead of choosing from 4 absolute directions (UP, DOWN, LEFT, RIGHT), the agent selects from **3 relative actions**:

| Action | Description |
|---|---|
| `AHEAD` | Continue in the current direction |
| `TURN_LEFT` | Turn 90 degrees to the left |
| `TURN_RIGHT` | Turn 90 degrees to the right |

This design inherently prevents the snake from reversing into itself (which would cause an immediate self-collision) and reduces the action space from 4 to 3.

### Reward System

The reward function shapes the agent's behavior through immediate feedback:

| Event | Reward | Rationale |
|---|---|---|
| Eat green apple | **+10.0** | Primary goal: grow the snake |
| Eat red apple | **-8.0** | Discourage shrinking |
| Normal move | **-0.4** | Penalize wandering to encourage efficiency |
| Game over (wall/self/zero) | **-20.0** | Strongly discourage death |
| Loop detected | **-4.0** | Penalize revisiting recent positions |

**Loop detection** uses a sliding window of the last 20 visited positions. If the snake revisits a position within this window, the loop penalty is applied. The window resets when a green apple is eaten.

### Q-Learning Algorithm

The agent uses tabular Q-learning with the following update rule:

```
Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
```

**Hyperparameters:**

| Parameter | Value | Description |
|---|---|---|
| `alpha` | 0.1 | Learning rate |
| `gamma` | 0.9 | Discount factor for future rewards |
| `epsilon` | 1.0 -> 0.05 | Exploration rate (epsilon-greedy) |
| `epsilon_decay` | Dynamic | Calculated so epsilon reaches `epsilon_min` at 80% of training |

**Exploration strategy**: The agent starts fully exploratory (epsilon = 1.0) and gradually shifts to exploitation. The decay rate is dynamically calculated so that epsilon reaches its minimum value at 80% of total training sessions, ensuring the final 20% of training is predominantly exploitation-based.

## Project Structure

```
learn2slither/
├── Makefile                       # Build and run targets
├── pyproject.toml                 # Project metadata and dependencies
├── docs/
│   └── en.subject.pdf             # 42 School project specification
├── models/                        # Saved Q-table snapshots
│   ├── q_learning_agent_10.json
│   ├── q_learning_agent_100.json
│   ├── q_learning_agent_1000.json
│   └── q_learning_agent_10000.json
├── src/
│   ├── main.py                    # CLI entry point
│   ├── config.py                  # Constants, enums, dataclasses
│   ├── agent/
│   │   ├── q_learning_agent.py    # Q-table agent (select, learn, save/load)
│   │   ├── reward.py              # Reward computation
│   │   └── trainer.py             # Training loop (episodes and steps)
│   ├── environment/
│   │   ├── board.py               # Grid board model
│   │   ├── snake.py               # Snake body (deque-based)
│   │   ├── apples.py              # Apple spawning logic
│   │   └── game.py                # Game state machine (step logic)
│   ├── state/
│   │   ├── vision.py              # Ray-casting vision system
│   │   └── encoder.py             # Rotation-invariant state encoding
│   ├── ui/
│   │   ├── app.py                 # Pygame UI entry point
│   │   ├── renderer.py            # Simple game renderer (CLI mode)
│   │   ├── screen_manager.py      # Screen stack manager
│   │   ├── theme.py               # Colors, fonts, layout constants
│   │   ├── widgets.py             # Reusable drawing helpers
│   │   └── screens/
│   │       ├── lobby_screen.py    # Main menu
│   │       ├── config_screen.py   # Hyperparameter configuration
│   │       ├── run_screen.py      # Live training/evaluation view
│   │       └── results_screen.py  # Post-training statistics
│   └── utils/
│       ├── arg_parser.py          # CLI argument parsing
│       └── training_report.py     # Metrics summary and printing
└── test/
    ├── test_board.py              # Board boundary tests
    ├── test_snake.py              # Snake model tests
    ├── test_apples.py             # Apple spawning tests
    ├── test_game.py               # Game logic tests
    ├── test_vision.py             # Vision ray-casting tests
    ├── test_encoder.py            # State encoder tests
    ├── test_q_learning_agent.py   # Agent behavior tests
    └── test_reward.py             # Reward computation tests
```

## Prerequisites

- **Python** >= 3.14
- **uv** — fast Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/burak-kayaa/learn2slither.git
   cd learn2slither
   ```

2. Install dependencies with uv:
   ```bash
   uv sync
   ```

   This installs:
   - `pygame` >= 2.6.1 — game rendering and UI
   - `pytest` >= 9.0.2 — testing framework
   - `flake8` >= 7.3.0 — code linting

## Usage

All commands are run through `uv` to ensure the correct virtual environment is used.

### Training a New Model

Train the agent headlessly (no visual output) for maximum speed:

```bash
uv run -m src.main --sessions 10000 --save trained_agent
```

This runs 10,000 episodes and saves the trained Q-table to `./models/q_learning_agent_10000.json`.

To watch the agent train in real time with visual rendering:

```bash
uv run -m src.main --sessions 1000 --render --delay 50
```

### Evaluating a Trained Model

Load a pre-trained model and watch it play without further learning:

```bash
uv run -m src.main --load ./models/q_learning_agent_10000.json --dont-learn --render --delay 1
```

Step through the game one move at a time for detailed inspection:

```bash
uv run -m src.main --load ./models/q_learning_agent_10000.json --dont-learn --render --step-by-step
```

### Graphical User Interface

Launch the full pygame UI with a lobby, configuration screen, live training view, and results dashboard:

```bash
uv run -m src.main --ui
```

The UI provides:

- **Lobby**: choose to train a new model, load an existing one, adjust configuration, or quit.
- **Configuration**: modify all hyperparameters (sessions, alpha, gamma, epsilon, decay, delay, etc.) using keyboard controls.
- **Run Screen**: watch the agent train/evaluate live with a real-time stats panel showing episode count, reward, epsilon, snake length, Q-table size, and a progress bar. Controls: `SPACE` to pause, `N` for next step, `S` to save, `ESC` to stop.
- **Results Screen**: view post-training statistics including average reward, best reward, average steps, death reason distribution, and a comparison between early and late episodes. Press `S` to save the model.

### CLI Reference

| Argument | Type | Default | Description |
|---|---|---|---|
| `--sessions` | int | 1000 | Number of training episodes |
| `--width` | int | 10 | Board width |
| `--height` | int | 10 | Board height |
| `--save` | str | — | Save trained agent to `./models/` |
| `--load` | str | — | Load a pre-trained agent from path |
| `--dont-learn` | flag | false | Disable learning (evaluation mode) |
| `--render` | flag | false | Enable pygame visual rendering |
| `--step-by-step` | flag | false | Wait for keypress between steps |
| `--delay` | int | 0 | Delay in ms between steps |
| `--ui` | flag | false | Launch the full pygame UI |

### Makefile Targets

| Target | Command | Description |
|---|---|---|
| `make` | `uv run -m src.main --sessions 10000 --save trained_agent.json` | Train for 10,000 episodes and save |
| `make load` | `uv run -m src.main --load ... --dont-learn --render --delay 1` | Load and visually evaluate the 10K model |
| `make ui` | `uv run -m src.main --ui` | Launch the graphical UI |
| `make t` | `uv run pytest` | Run all tests |

## Configuration

All game and training constants are centralized in `src/config.py`:

**Game Parameters:**

| Parameter | Value | Description |
|---|---|---|
| `BOARD_WIDTH` | 10 | Grid width |
| `BOARD_HEIGHT` | 10 | Grid height |
| `INITIAL_SNAKE_LENGTH` | 3 | Starting snake length |
| `GREEN_APPLE_COUNT` | 2 | Green apples on the board |
| `RED_APPLE_COUNT` | 1 | Red apples on the board |
| `MAX_STEPS_PER_EPISODE` | 400 | Step limit per episode (prevents infinite loops) |
| `LOOP_WINDOW` | 20 | Position history window for loop detection |

**Reward Values (`RewardConfig`):**

| Event | Reward |
|---|---|
| Green apple eaten | +10.0 |
| Red apple eaten | -8.0 |
| Normal step | -0.4 |
| Game over | -20.0 |
| Loop penalty | -4.0 |

**Agent Hyperparameters (`QLearningAgent` defaults):**

| Parameter | Default | Description |
|---|---|---|
| `alpha` | 0.1 | Learning rate |
| `gamma` | 0.9 | Discount factor |
| `epsilon` | 1.0 | Initial exploration rate |
| `epsilon_min` | 0.05 | Minimum exploration rate |
| `epsilon_decay` | 0.9997 | Per-episode decay (dynamically recalculated) |

## Pre-trained Models

Four model snapshots are included in the `models/` directory at different training stages:

| Model | Episodes | Q-table Size | Description |
|---|---|---|---|
| `q_learning_agent_10.json` | 10 | ~2 KB | Initial exploration, random behavior |
| `q_learning_agent_100.json` | 100 | ~5 KB | Early learning, basic wall avoidance |
| `q_learning_agent_1000.json` | 1,000 | ~138 KB | Intermediate, consistent apple-seeking |
| `q_learning_agent_10000.json` | 10,000 | ~210 KB | Fully trained, achieves lengths of 15-30+ |

Load any model with:
```bash
uv run -m src.main --load ./models/q_learning_agent_10000.json --dont-learn --render --delay 1
```

## Testing

The test suite covers all core modules with 35 tests:

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run a specific test file
uv run pytest test/test_game.py
```

| Test File | Tests | Coverage |
|---|---|---|
| `test_board.py` | 4 | Board bounds checking, dimension validation |
| `test_snake.py` | 7 | Movement, growth, shrinking, position tracking |
| `test_apples.py` | 3 | Apple spawning, no overlap with snake |
| `test_game.py` | 7 | Wall collision, self collision, apple eating, zero length |
| `test_vision.py` | 2 | Ray-casting correctness |
| `test_encoder.py` | 3 | Rotation-invariant encoding for different directions |
| `test_q_learning_agent.py` | 8 | Exploration, exploitation, Q-update, epsilon decay, save/load |
| `test_reward.py` | 1 | Reward values for all event types |

## Architecture

### Training Loop

The training process follows this cycle for each episode:

```
for each episode:
    reset environment
    while not game_over:
        1. Cast rays from snake head in 4 directions     [VisionInterpreter]
        2. Encode vision into rotation-invariant state    [StateEncoder]
        3. Select relative action (epsilon-greedy)        [QLearningAgent]
        4. Convert relative action to absolute direction  [config.RELATIVE_TO_ABSOLUTE]
        5. Execute action in the environment              [Game.step()]
        6. Compute reward from step result                [compute_reward()]
        7. Apply loop penalty if revisiting positions     [Trainer]
        8. Update Q-table with (s, a, r, s')              [QLearningAgent.learn()]
    decay epsilon
```

### Key Design Decisions

1. **Relative actions over absolute directions**: The agent chooses from 3 relative actions (AHEAD, TURN_LEFT, TURN_RIGHT) instead of 4 absolute directions. This eliminates the possibility of self-reversal and reduces the action space.

2. **Rotation-invariant state encoding**: Vision is encoded relative to the snake's current heading (ahead/left/right), so the agent learns generalizable patterns independent of absolute orientation. This significantly reduces the Q-table size.

3. **Bucketed distances**: Raw cell distances are bucketed into CLOSE (1), NEAR (2-3), and FAR (4+) categories. This compresses the state space while preserving actionable spatial information.

4. **Loop penalty with sliding window**: A deque of the last 20 positions detects repetitive movement. Revisiting a position within this window incurs a -4.0 penalty, discouraging circular behavior.

5. **Dynamic epsilon decay**: Rather than using a fixed decay rate, the trainer calculates the decay so that epsilon reaches its minimum at exactly 80% of total training, ensuring the final 20% focuses on exploitation.

6. **Threaded UI rendering**: The RunScreen executes the training loop in a background thread, keeping the pygame event loop responsive during training.
