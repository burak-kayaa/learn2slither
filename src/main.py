from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.agent.q_learning_agent import QLearningAgent
from src.agent.reward import compute_reward
from src.agent.trainer import run_episode, train
from src.utils.training_report import summarize_metrics, death_reason_counts

def main():
    env = Game()
    agent = QLearningAgent()
    sessions = 10000

    episode_metrics_list = train(env, agent, sessions)

    first_100 = episode_metrics_list[:100]
    last_100 = episode_metrics_list[-100:]

    print("FIRST 100:", summarize_metrics(first_100))
    print("LAST 100:", summarize_metrics(last_100))
    print("DEATH REASONS:", death_reason_counts(episode_metrics_list))
    print("FINAL EPSILON:", agent.epsilon)
    print("Q-TABLE SIZE:", len(agent.q_table))

if __name__ == "__main__":
    main()