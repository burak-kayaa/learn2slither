"""Application entry point for the pygame UI."""

from __future__ import annotations

from src.ui.screen_manager import ScreenManager
from src.ui.screens.lobby_screen import LobbyScreen


DEFAULT_CONFIG: dict = {
    "sessions": 10000,
    "alpha": 0.1,
    "gamma": 0.9,
    "epsilon": 1.0,
    "epsilon_decay": 0.9997,
    "epsilon_min": 0.05,
    "delay_ms": 1,
    "step_mode": False,
    "dont_learn": False,
    "visual": True,
    "mode": "train",
    "load_path": "",
    "save_path": "",
}


def run_app() -> None:
    app_config = dict(DEFAULT_CONFIG)
    sm = ScreenManager()
    sm.push(LobbyScreen(sm, app_config))
    sm.run()
