from src.config import BOARD_HEIGHT, BOARD_WIDTH
from src.environment.game import Game
from src.agent.q_learning_agent import QLearningAgent
from src.agent.trainer import train
from src.ui.renderer import GameRenderer, RenderConfig
from src.utils.arg_parser import parse_args
from src.utils.training_report import (
    print_metrics_summary,
    summarize_metrics
)
from src.ui.app import run_app


def main():
    args = parse_args()
    if args.ui:
        run_app()
        return
    env = Game(
        width=args.width if args.width else BOARD_WIDTH,
        height=args.height if args.height else BOARD_HEIGHT
    )
    renderer = GameRenderer(
        args.width if args.width else BOARD_WIDTH,
        args.height if args.height else BOARD_HEIGHT,
        RenderConfig(
            delay_ms=args.delay if not args.step_by_step else 0,
            step_mode=args.step_by_step,
            enabled=args.render
        )
    )
    if args.load:
        agent = QLearningAgent.load(args.load)
    else:
        agent = QLearningAgent()
    if args.dont_learn:
        agent.learning_enabled = False
    metrics = train(env, agent, args.sessions,
                    renderer if args.render else None)
    if args.save:
        agent.save(args.sessions)
    print_metrics_summary(summarize_metrics(metrics))


if __name__ == "__main__":
    main()
