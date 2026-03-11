from src.agent.reward import compute_reward
from src.config import RewardConfig, StepResult, Event


def test_compute_reward():
    sr = StepResult
    step = RewardConfig.step
    assert compute_reward(sr(event=Event.GREEN_APPLE, done=False)) == 10.0
    assert compute_reward(sr(event=Event.RED_APPLE, done=False)) == -8.0
    assert compute_reward(sr(event=Event.MOVE, done=False)) == step
    assert compute_reward(sr(event=Event.WALL_COLLISION, done=True)) == -20.0
    assert compute_reward(sr(event=Event.SELF_COLLISION, done=True)) == -20.0
    assert compute_reward(sr(event=Event.ZERO_LENGTH, done=True)) == -20.0
    assert compute_reward(sr(event=Event.GAME_ALREADY_OVER, done=True)) == 0.0
