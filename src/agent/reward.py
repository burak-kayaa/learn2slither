from src.config import RewardConfig, StepResult, Event


def compute_reward(step_result: StepResult) -> float:
    if step_result.event == Event.GREEN_APPLE:
        return RewardConfig.green_apple
    if step_result.event == Event.RED_APPLE:
        return RewardConfig.red_apple
    if step_result.event == Event.MOVE:
        return RewardConfig.step
    if step_result.event in {
        Event.WALL_COLLISION,
        Event.SELF_COLLISION,
        Event.ZERO_LENGTH,
    }:
        return RewardConfig.game_over
    if step_result.event == Event.GAME_ALREADY_OVER:
        return 0.0
    raise ValueError(f"Unknown event: {step_result.event}")
