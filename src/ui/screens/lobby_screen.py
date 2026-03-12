"""Lobby / main menu screen."""

from __future__ import annotations

import pygame
from src.ui import theme
from src.ui.screen_manager import Screen, ScreenManager
from src.ui.widgets import draw_text_centered, draw_menu_item
from src.ui.screens.config_screen import ConfigScreen
from src.ui.screens.run_screen import RunScreen


_MENU_ITEMS = [
    "Train New Model",
    "Load Model & Evaluate",
    "Configuration",
    "Quit",
]


class LobbyScreen(Screen):
    def __init__(self, manager: ScreenManager, app_config: dict) -> None:
        super().__init__(manager)
        self.app_config = app_config
        self.selected = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(_MENU_ITEMS)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(_MENU_ITEMS)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._activate()

    def _activate(self) -> None:
        choice = _MENU_ITEMS[self.selected]
        if choice == "Train New Model":
            self.app_config["mode"] = "train"
            self.manager.push(RunScreen(self.manager, self.app_config))
        elif choice == "Load Model & Evaluate":
            self.app_config["mode"] = "evaluate"
            self.manager.push(ConfigScreen(self.manager, self.app_config))
        elif choice == "Configuration":
            self.manager.push(ConfigScreen(self.manager, self.app_config))
        elif choice == "Quit":
            self.manager.running = False

    def draw(self, surface: pygame.Surface) -> None:
        draw_text_centered(
            surface, "Learn2Slither", 120,
            theme.ACCENT, 52, bold=True,
        )
        draw_text_centered(
            surface, "Reinforcement Learning Snake Simulator", 185,
            theme.TEXT_DIM, 18,
        )
        menu_x = surface.get_width() // 2 - 180
        menu_w = 360
        y = 280
        for i, label in enumerate(_MENU_ITEMS):
            draw_menu_item(
                surface, label, menu_x, y, menu_w,
                selected=(i == self.selected),
            )
            y += 56

        draw_text_centered(
            surface,
            "↑↓  Navigate    Enter  Select",
            theme.WINDOW_H - 40,
            theme.TEXT_DIM, 14,
        )
