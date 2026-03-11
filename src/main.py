from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.agent.q_learning_agent import QLearningAgent
from src.agent.reward import compute_reward
from src.agent.trainer import run_episode, train
from src.utils.arg_parser import parse_args
from src.utils.training_report import print_metrics_summary, summarize_metrics, death_reason_counts


def main():
    args = parse_args()
    env = Game()
    if args.load:
        agent = QLearningAgent.load(args.load)
    else:
        agent = QLearningAgent()
    if args.dontlearn:
        agent.learning_enabled = False
    metrics = train(env, agent, args.sessions)
    if args.save:
        agent.save(args.sessions)
    print_metrics_summary(summarize_metrics(metrics))

if __name__ == "__main__":
    main()