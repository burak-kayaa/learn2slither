from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder
from src.agent.q_learning_agent import QLearningAgent
from src.agent.reward import compute_reward

def main():
    game = Game(width=5, height=5)
    game.board.print_board(game.snake.as_list(), game.green_apples, game.red_apple)
    vision = VisionInterpreter.extract(game)
    state = StateEncoder.encode(vision)
    agent = QLearningAgent(q_table={})
    action_values = agent.get_action_values(state)
    print("Action values:", action_values)
    step_result = game.step("UP")
    print("Step result:", step_result)
    

if __name__ == "__main__":
    main()