from typing import Union, Tuple
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, BLOCK_SIZE


class GameObjectBase:
    def __init__(self, screen: Union[pygame.Surface, pygame.SurfaceType], color: Tuple[int, int, int]):
        self._screen = screen
        self._block_size = BLOCK_SIZE
        self._color = color

    def _draw(self, coordinate: Tuple[int, int], color=None) -> pygame.Rect or pygame.rect.RectType:
        if color is None:
            color = self._color
        x, y = coordinate
        return pygame.draw.rect(self._screen, color, (x, y, self._block_size, self._block_size))

    def _check_position(self, position: Tuple[int, int]) -> bool:
        x, y = position

        if x < 0 or y < 0:
            return False

        if x > SCREEN_WIDTH - self._block_size or y > SCREEN_HEIGHT - self._block_size:
            return False

        return True

    def _clear_position(self, position: Tuple[int, int]):
        self._draw(position, BLACK)
