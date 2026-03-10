from src.environment.board import Board
from src.environment.game import Game
from src.state.vision import VisionInterpreter
from src.state.encoder import StateEncoder

def main():
    game = Game(width=5, height=5)
    game.board.print_board(game.snake.as_list(), game.green_apples, game.red_apple)
    vision = VisionInterpreter.extract(game)
    print(StateEncoder.encode(vision))
    print("---")

if __name__ == "__main__":
    main()