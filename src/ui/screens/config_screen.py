"""Configuration panel screen."""

from __future__ import annotations

import pygame
from src.ui import theme
from src.ui.screen_manager import Screen, ScreenManager
from src.ui.widgets import (
    draw_menu_item, draw_text, draw_text_centered, draw_panel,
)


_FIELDS: list[tuple[str, str, str, float, float, float]] = [
    ("sessions",      "Sessions",       "int",    1000,   100,  500_000),
    ("alpha",         "Alpha (LR)",     "float",  0.01,   0.01, 1.0),
    ("gamma",         "Gamma",          "float",  0.05,   0.0,  1.0),
    ("epsilon",       "Epsilon",        "float",  0.05,   0.0,  1.0),
    ("epsilon_decay",  "Eps. Decay",    "float",  0.0001, 0.9,  1.0),
    ("epsilon_min",   "Eps. Min",       "float",  0.01,   0.0,  1.0),
    ("delay_ms",      "Delay (ms)",     "int",    10,     0,    1000),
    ("step_mode",     "Step Mode",      "bool",   0,      0,    1),
    ("dont_learn",    "Don't Learn",    "bool",   0,      0,    1),
    ("visual",        "Visual",         "bool",   0,      0,    1),
]

_ACTIONS = [
    "Start Training",
    "Start Evaluation",
    "Back",
]


class ConfigScreen(Screen):
    def __init__(self, manager: ScreenManager, app_config: dict) -> None:
        super().__init__(manager)
        self.app_config = app_config
        self.selected = 0
        self.total_rows = len(_FIELDS) + len(_ACTIONS)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.manager.pop()
            return
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % self.total_rows
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % self.total_rows
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self._adjust(event.key)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._activate()

    def _adjust(self, key: int) -> None:
        if self.selected >= len(_FIELDS):
            return
        cfg_key, _, ftype, step, lo, hi = _FIELDS[self.selected]
        val = self.app_config.get(cfg_key, 0)
        if ftype == "bool":
            self.app_config[cfg_key] = not val
            return
        delta = step if key == pygame.K_RIGHT else -step
        if ftype == "int":
            self.app_config[cfg_key] = int(max(lo, min(hi, val + delta)))
        else:
            self.app_config[cfg_key] = round(
                max(lo, min(hi, val + delta)), 4,
            )

    def _activate(self) -> None:
        if self.selected < len(_FIELDS):
            field = _FIELDS[self.selected]
            if field[2] == "bool":
                key = field[0]
                self.app_config[key] = not self.app_config.get(key, False)
            return
        action = _ACTIONS[self.selected - len(_FIELDS)]
        if action == "Back":
            self.manager.pop()
        elif action == "Start Training":
            from src.ui.screens.run_screen import RunScreen
            self.app_config["mode"] = "train"
            self.manager.push(RunScreen(self.manager, self.app_config))
        elif action == "Start Evaluation":
            from src.ui.screens.run_screen import RunScreen
            self.app_config["mode"] = "evaluate"
            self.manager.push(RunScreen(self.manager, self.app_config))

    def draw(self, surface: pygame.Surface) -> None:
        draw_text_centered(
            surface, "Configuration", 30, theme.ACCENT, 32, bold=True,
        )
        panel = pygame.Rect(80, 80, surface.get_width() - 160, 580)
        draw_panel(surface, panel)
        x, y = panel.x + 24, panel.y + 20
        w = panel.width - 48
        for i, (cfg_key, label, ftype, *_) in enumerate(_FIELDS):
            sel = i == self.selected
            row_rect = pygame.Rect(x - 8, y, w + 16, 36)
            if sel:
                pygame.draw.rect(
                    surface, theme.HIGHLIGHT, row_rect, border_radius=4,
                )
            val = self.app_config.get(cfg_key, "")
            if ftype == "bool":
                val_str = "ON" if val else "OFF"
                val_color = theme.SUCCESS if val else theme.TEXT_DIM
            elif ftype == "float":
                val_str = f"{val:.4f}"
                val_color = theme.TEXT
            else:
                val_str = str(val)
                val_color = theme.TEXT
            lbl_color = theme.ACCENT if sel else theme.TEXT_DIM
            draw_text(surface, label, x, y + 6, lbl_color, 18)
            draw_text(
                surface, f"◀  {val_str}  ▶" if sel else val_str,
                x + w, y + 6, val_color, 18, anchor="topright",
            )
            y += 40

        y += 16
        for j, action_label in enumerate(_ACTIONS):
            idx = len(_FIELDS) + j
            draw_menu_item(
                surface, action_label, x, y, w,
                selected=(idx == self.selected), size=22,
            )
            y += 48

        draw_text_centered(
            surface,
            "↑↓  Navigate    ◀▶  Adjust    Enter  Select    Esc  Back",
            theme.WINDOW_H - 40,
            theme.TEXT_DIM, 14,
        )
