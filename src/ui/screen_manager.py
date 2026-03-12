"""Minimal screen manager: holds a stack of screens, delegates events."""

from __future__ import annotations

import pygame
from src.ui import theme


class Screen:
    """Base class every screen subclasses."""

    def __init__(self, manager: ScreenManager) -> None:
        self.manager = manager

    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    def update(self) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        ...


class ScreenManager:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(
            (theme.WINDOW_W, theme.WINDOW_H),
        )
        pygame.display.set_caption("Learn2Slither")
        self.clock = pygame.time.Clock()
        self._stack: list[Screen] = []
        self.running = True

    @property
    def current(self) -> Screen | None:
        return self._stack[-1] if self._stack else None

    def push(self, screen: Screen) -> None:
        self._stack.append(screen)

    def pop(self) -> None:
        if self._stack:
            self._stack.pop()
        if not self._stack:
            self.running = False

    def replace(self, screen: Screen) -> None:
        if self._stack:
            self._stack.pop()
        self._stack.append(screen)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if self.current:
                    self.current.handle_event(event)
            if not self.running:
                break
            if self.current:
                self.current.update()
                self.surface.fill(theme.BG)
                self.current.draw(self.surface)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
