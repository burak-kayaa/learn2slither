from environment.board import Board
from environment.game import Game
from state.vision import VisionInterpreter

def main():
    game = Game(width=5, height=5)
    game.board.print_board(game.snake.as_list(), game.green_apples, game.red_apple)
    vision = VisionInterpreter.extract(game)
    VisionInterpreter.print_vision(vision)
    print("---")

if __name__ == "__main__":
    main()