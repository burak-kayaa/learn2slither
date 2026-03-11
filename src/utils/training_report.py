from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MetricsSummary:
    episodes: int
    avg_steps: float
    avg_reward: float
    avg_max_length: float
    avg_green_apples: float
    avg_red_apples: float


def average_metric(metrics_list: list[Any], attr_name: str) -> float:
    if not metrics_list:
        return 0.0
    return sum(getattr(m, attr_name) for m in metrics_list) / len(metrics_list)


def summarize_metrics(metrics_list: list[Any]) -> MetricsSummary:
    return MetricsSummary(
        episodes=len(metrics_list),
        avg_steps=average_metric(metrics_list, "steps"),
        avg_reward=average_metric(metrics_list, "total_reward"),
        avg_max_length=average_metric(metrics_list, "max_length"),
        avg_green_apples=average_metric(metrics_list, "green_apples_eaten"),
        avg_red_apples=average_metric(metrics_list, "red_apples_eaten"),
    )


def death_reason_counts(metrics_list: list[Any]) -> dict[str, int]:
    counter = Counter(str(m.death_reason) for m in metrics_list)
    return dict(counter)