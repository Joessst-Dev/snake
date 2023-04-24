import pygame
from typing import Union, List
from config import SCREEN_HEIGHT, SCREEN_WIDTH, GREEN
from food import Food
from game_object import GameObjectBase


class Snake(GameObjectBase):
    def __init__(self, screen: Union[pygame.Surface, pygame.SurfaceType]):
        super().__init__(screen, GREEN)
        self.body = []
        self.head = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.body.append(self.head)
        self.rectangles: List[pygame.rect.Rect or pygame.rect.RectType] = []
        self.direction = "right"
        self.length = 1

    def draw(self):
        self.rectangles = [self._draw(coordinate) for coordinate in self.body]

    def move(self):
        x, y = self.head
        if self.direction == "right":
            x += self._block_size
        elif self.direction == "left":
            x -= self._block_size
        elif self.direction == "up":
            y -= self._block_size
        elif self.direction == "down":
            y += self._block_size

        self.head = (x, y)
        self.body.insert(0, self.head)

        if len(self.body) > self.length:
            removed_coordinate = self.body.pop()
            self._clear_position(removed_coordinate)

    def change_direction(self, direction: str):
        if direction == "right" and self.direction != "left":
            self.direction = "right"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"

    def grow(self):
        tail_x, tail_y = self.body[-1]
        if self.direction == "up":
            coordinate = (tail_x, tail_y - self._block_size)
        elif self.direction == "down":
            coordinate = (tail_x, tail_y + self._block_size)
        elif self.direction == "left":
            coordinate = (tail_x + self._block_size, tail_y)
        elif self.direction == "right":
            coordinate = (tail_x - self._block_size, tail_y)
        else:
            raise Exception('invalid direction')
        self.body.append(coordinate)
        self.length += 1

    def check_food(self, food: Food) -> bool:
        if len(self.body) > 0:
            head_x, head_y = self.head
            food_x, food_y = food.position
            if head_x == food_x and head_y == food_y:
                self.grow()
                food.remove()
                return True
        return False

    def check_collision(self) -> bool:
        # check if snake is out of field
        if self._check_position(self.head) is False:
            return True

        # check if snake has a collision with itself
        # if len(self.rectangles) > 0:
        #     body_rectangles = self.rectangles[3:]
        #     head = self.rectangles[0]
        #
        #     for rect in body_rectangles:
        #         if head.colliderect(rect):
        #             return True

        if len(self.body) > 0:
            filtered_body = self.body[1:]
            head_x, head_y = self.head

            for body_part in filtered_body:
                body_x, body_y = body_part
                if body_x == head_x and body_y == head_y:
                    return True

        return False
