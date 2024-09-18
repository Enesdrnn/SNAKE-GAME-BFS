from snake import *
from os import environ


def draw_screen(surface):
    surface.fill(SURFACE_CLR)


def draw_grid(surface):
    x = 0
    y = 0
    for r in range(ROWS):
        x = x + SQUARE_SIZE
        y = y + SQUARE_SIZE
        pygame.draw.line(surface, GRID_CLR, (x, 0), (x, HEIGHT))
        pygame.draw.line(surface, GRID_CLR, (0, y), (WIDTH, y))


def play_game():
    pygame.init()
    environ['merkez'] = '1'
    pygame.display.set_caption("Snake Game")
    oyun_yüzeyi = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(oyun_yüzeyi)

    mainloop = True
    while mainloop:
        draw_screen(oyun_yüzeyi)
        draw_grid(oyun_yüzeyi)

        snake.update()

        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    play_game()
