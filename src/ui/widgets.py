"""Reusable pygame drawing helpers."""

from __future__ import annotations

import pygame
from src.ui import theme


# ── Text ──────────────────────────────────────────────────────────────
def draw_text(
    surface: pygame.Surface,
    text: str,
    x: int,
    y: int,
    color: tuple = theme.TEXT,
    size: int = 20,
    bold: bool = False,
    anchor: str = "topleft",
) -> pygame.Rect:
    f = theme.font(size, bold)
    rendered = f.render(text, True, color)
    rect = rendered.get_rect(**{anchor: (x, y)})
    surface.blit(rendered, rect)
    return rect


def draw_text_centered(
    surface: pygame.Surface,
    text: str,
    y: int,
    color: tuple = theme.TEXT,
    size: int = 20,
    bold: bool = False,
) -> pygame.Rect:
    return draw_text(
        surface, text,
        surface.get_width() // 2, y,
        color, size, bold,
        anchor="midtop",
    )


# ── Panel ─────────────────────────────────────────────────────────────
def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    border: bool = True,
) -> None:
    pygame.draw.rect(surface, theme.PANEL_BG, rect, border_radius=6)
    if border:
        pygame.draw.rect(
            surface, theme.PANEL_BORDER, rect, width=1, border_radius=6,
        )


# ── Stat row  (label: value) ─────────────────────────────────────────
def draw_stat_row(
    surface: pygame.Surface,
    x: int,
    y: int,
    label: str,
    value: str,
    width: int = 300,
    label_color: tuple = theme.TEXT_DIM,
    value_color: tuple = theme.TEXT,
    size: int = 18,
) -> int:
    draw_text(surface, label, x, y, label_color, size)
    draw_text(
        surface, value, x + width, y, value_color, size, anchor="topright"
    )
    return y + size + 6


# ── Menu item ─────────────────────────────────────────────────────────
def draw_menu_item(
    surface: pygame.Surface,
    text: str,
    x: int,
    y: int,
    width: int,
    selected: bool = False,
    size: int = 24,
) -> pygame.Rect:
    h = size + 16
    rect = pygame.Rect(x, y, width, h)
    if selected:
        pygame.draw.rect(surface, theme.HIGHLIGHT, rect, border_radius=4)
        pygame.draw.rect(surface, theme.ACCENT, rect, width=2, border_radius=4)
    color = theme.ACCENT if selected else theme.TEXT
    draw_text(surface, text, x + 16, y + 8, color, size, bold=selected)
    return rect


# ── Horizontal bar chart ─────────────────────────────────────────────
def draw_bar_chart(
    surface: pygame.Surface,
    x: int,
    y: int,
    width: int,
    height: int,
    data: list[tuple[str, float]],
    title: str = "",
    bar_color: tuple = theme.CHART_BAR,
) -> int:
    if title:
        draw_text(surface, title, x, y, theme.TEXT, 16, bold=True)
        y += 22
    if not data:
        return y
    max_val = max(abs(v) for _, v in data) or 1
    bar_h = min(22, (height - 22) // len(data) - 4)
    for label, val in data:
        draw_text(surface, label, x, y + 2, theme.TEXT_DIM, 14)
        bar_x = x + 110
        bar_w = int((val / max_val) * (width - 130))
        bar_w = max(bar_w, 2)
        pygame.draw.rect(
            surface, bar_color,
            (bar_x, y + 2, bar_w, bar_h),
            border_radius=3,
        )
        draw_text(
            surface, f"{val:.1f}",
            bar_x + bar_w + 6, y + 2, theme.TEXT, 14,
        )
        y += bar_h + 6
    return y


# ── Comparison two-bar chart (first vs last) ─────────────────────────
def draw_comparison_bars(
    surface: pygame.Surface,
    x: int,
    y: int,
    width: int,
    labels: list[str],
    first_vals: list[float],
    last_vals: list[float],
    title: str = "",
) -> int:
    if title:
        draw_text(surface, title, x, y, theme.TEXT, 16, bold=True)
        y += 22

    draw_text(surface, "■ First 100", x + width - 180, y, theme.ACCENT_DIM, 12)
    draw_text(surface, "■ Last 100", x + width - 90, y, theme.SUCCESS, 12)
    y += 18

    all_vals = first_vals + last_vals
    max_val = max(abs(v) for v in all_vals) if all_vals else 1
    max_val = max_val or 1
    bar_h = 10
    for i, label in enumerate(labels):
        draw_text(surface, label, x, y + 2, theme.TEXT_DIM, 14)
        bar_x = x + 130
        avail = width - 150

        w1 = max(int((first_vals[i] / max_val) * avail), 2)
        pygame.draw.rect(
            surface, theme.ACCENT_DIM, (bar_x, y, w1, bar_h), border_radius=2,
        )
        draw_text(
            surface, f"{first_vals[i]:.1f}",
            bar_x + w1 + 4, y - 1, theme.TEXT_DIM, 12,
        )

        w2 = max(int((last_vals[i] / max_val) * avail), 2)
        pygame.draw.rect(
            surface, theme.SUCCESS,
            (bar_x, y + bar_h + 2, w2, bar_h), border_radius=2,
        )
        draw_text(
            surface, f"{last_vals[i]:.1f}",
            bar_x + w2 + 4, y + bar_h + 1, theme.SUCCESS, 12,
        )

        y += bar_h * 2 + 12
    return y
