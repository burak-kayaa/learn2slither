import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a Q-learning agent to play Slither.io"
    )
    parser.add_argument("--sessions", type=int, default=1000,
                        help="Number of training sessions (episodes)")
    parser.add_argument(
        "--save", type=str, help="Path to save the trained agent"
    )
    parser.add_argument(
        "--load", type=str, help="Path to load a pre-trained agent"
    )
    parser.add_argument("--dont-learn", action="store_true",
                        help="Disable learning (useful for evaluation)")
    parser.add_argument("--render", action="store_true",
                        help="Render the game during training")
    parser.add_argument(
        "--step-by-step", action="store_true",
        help="Wait for user input between steps when rendering"
    )
    parser.add_argument(
        "--delay", type=int, default=0,
        help="Delay in ms between steps (overridden by --step-by-step)"
    )
    parser.add_argument(
        "--ui", action="store_true",
        help="Launch the full pygame UI (lobby, config, run, results)"
    )
    return parser.parse_args()
