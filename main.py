import random
import sys
import pygame
from typing import Union, Tuple
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, TICK_RATE, DEBUGGING_TEXT, RED, BLACK, PURPLE
from food import Food
from snake import Snake

# initialisiert alle pygame Module
pygame.init()


# initialisiert das Spiel
def setup_game(title='Snake Game'):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(title)
    return screen


def place_food(snake: Snake, screen: Union[pygame.Surface, pygame.SurfaceType]) -> Food:
    def _generate_food():
        x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * float(BLOCK_SIZE)
        y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * float(BLOCK_SIZE)

        # prüfen ob die neuen Food-Koordinaten in der Schlange liegt
        for body_part in snake.body:
            body_x, body_y = body_part
            if body_x == x and body_y == y:
                return _generate_food()
        return x, y

    food_coordinate = _generate_food()
    food = Food(screen, food_coordinate)
    return food


def write_text_left_corner(text: str, screen: Union[pygame.Surface, pygame.SurfaceType], font: pygame.font.Font, color: Tuple[int, int, int]):
    rendered_text, text_rect = get_rendered_text(text, font, color)
    text_rect.topleft = screen.get_rect().topleft
    screen.blit(rendered_text, text_rect)


def write_text_right_corner(text: str, screen: Union[pygame.Surface, pygame.SurfaceType], font: pygame.font.Font, color: Tuple[int, int, int]):
    rendered_text, text_rect = get_rendered_text(text, font, color)
    text_rect.topright = screen.get_rect().topright
    screen.blit(rendered_text, text_rect)


def write_text_center(text: str, screen: Union[pygame.Surface, pygame.SurfaceType], font: pygame.font.Font, color: Tuple[int, int, int]):
    rendered_text, text_rect = get_rendered_text(text, font, color)
    text_rect.center = screen.get_rect().center
    screen.blit(rendered_text, text_rect)


def get_rendered_text(text: str, font: pygame.font.Font, color: Tuple[int, int, int]) -> Tuple[Union[pygame.Surface, pygame.SurfaceType], Union[pygame.Rect, pygame.rect.RectType]]:
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect()
    return rendered_text, text_rect


# main function
def main():
    screen = setup_game()
    snake = Snake(screen)
    current_food = place_food(snake, screen)
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 14)
    food_counter = 0
    game_over = False
    close_game = False

    while close_game is False:
        # game over loop
        while game_over is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
                    elif event.key == pygame.K_q:
                        game_over = False
                        close_game = True

            screen.fill(BLACK)
            write_text_center('GAME OVER - Leertaste = play Q = Verlassen', screen, font_big, RED)
            write_text_right_corner(f'food counter: {food_counter}', screen, font_big, RED)
            pygame.display.update()
            clock.tick(TICK_RATE)

        # Events behandeln (Bewegung der Schlange oder beenden des Spiels
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("right")

        # updaten des game states
        snake.move()
        if snake.check_collision():
            game_over = True
        food_collision = snake.check_food(current_food)
        if food_collision is True:
            current_food = place_food(snake, screen)
            food_counter += 1

        # Das Fenster neu zeichnen
        screen.fill(BLACK)
        snake.draw()
        current_food.draw()
        if DEBUGGING_TEXT:
            text = f'snake-x: {snake.head[0]}, snake-y: {snake.head[1]}, food-x: {current_food.position[0]}, food-y: {current_food.position[1]}'
            write_text_left_corner(text, screen, font_small, RED)
        write_text_right_corner(f'food counter: {food_counter}', screen, font_big, PURPLE)

        # das Fenster mit neu gezeichneten Inhalten updaten
        pygame.display.update()

        clock.tick(TICK_RATE)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
