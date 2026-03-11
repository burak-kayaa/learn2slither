import pygame

from src.config import Colors, RenderConfig


class GameRenderer:
    def __init__(
        self, board_width: int, board_height: int, config: RenderConfig
    ):
        self.board_width = board_width
        self.board_height = board_height
        self.config = config
        self.initialized = False
        self.clock = None

    def initialize(self) -> None:
        if not self.config.enabled or self.initialized:
            return
        pygame.init()
        width = self.board_width * self.config.cell_size
        height = self.board_height * self.config.cell_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Learn2Slither")
        self.initialized = True

    def render(self, env) -> None:
        if not self.config.enabled:
            return
        if not self.initialized:
            self.initialize()
        self._handle_basic_events()
        self.screen.fill(Colors.BACKGROUND)
        self._draw_grid()
        self._draw_apples(env)
        self._draw_snake(env)
        pygame.display.flip()
        if self.config.step_mode:
            self.wait_for_step()
        elif self.config.delay_ms > 0:
            pygame.time.delay(self.config.delay_ms)

    def wait_for_step(self) -> None:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def _draw_grid(self) -> None:
        cell = self.config.cell_size
        color = Colors.GRID
        for y in range(self.board_height):
            for x in range(self.board_width):
                rect = pygame.Rect(x * cell, y * cell, cell, cell)
                pygame.draw.rect(self.screen, color, rect, 1)

    def _draw_snake(self, env) -> None:
        cell = self.config.cell_size
        body_color = Colors.SNAKE
        head_color = Colors.SNAKE_HEAD
        snake_positions = env.snake.as_list()
        for index, (x, y) in enumerate(snake_positions):
            rect = pygame.Rect(x * cell, y * cell, cell, cell)
            color = head_color if index == 0 else body_color
            pygame.draw.rect(self.screen, color, rect)

    def _draw_apples(self, env) -> None:
        cell = self.config.cell_size
        for (x, y) in env.green_apples:
            rect = pygame.Rect(x * cell, y * cell, cell, cell)
            pygame.draw.rect(self.screen, Colors.GREEN_APPLE, rect)
        if env.red_apple is not None:
            x, y = env.red_apple
            rect = pygame.Rect(x * cell, y * cell, cell, cell)
            pygame.draw.rect(self.screen, Colors.RED_APPLE, rect)

    def _handle_basic_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
