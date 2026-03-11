import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train a Q-learning agent to play Slither.io")
    parser.add_argument("--sessions", type=int, default=1000, help="Number of training sessions (episodes)")
    parser.add_argument("--save", type=str, help="Path to save the trained agent")
    parser.add_argument("--load", type=str, help="Path to load a pre-trained agent")
    parser.add_argument("--dontlearn", action="store_true", help="Disable learning (useful for evaluation)")
    parser.add_argument("--render", action="store_true", help="Render the game during training")
    return parser.parse_args()