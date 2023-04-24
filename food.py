import pygame
from typing import Union, Tuple
from config import RED
from game_object import GameObjectBase


class Food(GameObjectBase):
    def __init__(self, screen: Union[pygame.Surface, pygame.SurfaceType], position: Tuple[int, int]):
        super().__init__(screen, RED)
        self.position = position
        self.rect: pygame.rect.Rect or pygame.rect.RectType or None = None

        if self._check_position(position) is False:
            print(f"invalid position {position}")
            raise Exception()

    def draw(self):
        self.rect = self._draw(self.position)

    def remove(self):
        self._clear_position(self.position)
