"""Central color and font theme for the entire UI."""

import pygame


# ── Colors ────────────────────────────────────────────────────────────
BG = (18, 18, 24)
PANEL_BG = (28, 28, 38)
PANEL_BORDER = (55, 55, 75)
TEXT = (220, 220, 230)
TEXT_DIM = (130, 130, 150)
ACCENT = (80, 160, 255)
ACCENT_DIM = (50, 100, 180)
HIGHLIGHT = (45, 45, 65)
SUCCESS = (60, 200, 100)
DANGER = (220, 60, 60)
WARNING = (240, 180, 40)
GREEN_APPLE = (30, 200, 80)
RED_APPLE = (220, 50, 50)
SNAKE_BODY = (50, 120, 255)
SNAKE_HEAD = (100, 180, 255)
GRID_LINE = (40, 40, 55)
EMPTY_CELL = (24, 24, 32)
CHART_BAR = (80, 160, 255)
CHART_BAR_ALT = (60, 200, 100)

# ── Font cache ────────────────────────────────────────────────────────
_font_cache: dict = {}


def font(size: int = 20, bold: bool = False):
    key = (size, bold)
    if key not in _font_cache:
        f = pygame.font.SysFont("consolas,dejavusansmono,monospace", size)
        f.set_bold(bold)
        _font_cache[key] = f
    return _font_cache[key]


# ── Layout constants ─────────────────────────────────────────────────
WINDOW_W = 1280
WINDOW_H = 780
BOARD_AREA_W = 620
SIDE_PANEL_W = WINDOW_W - BOARD_AREA_W
PAD = 16
CELL_SIZE = 56
BOARD_OFFSET_X = (BOARD_AREA_W - 10 * CELL_SIZE) // 2
BOARD_OFFSET_Y = 60
