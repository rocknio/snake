import pygame
import sys
from pygame.locals import *

from my_snake import MySnake

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("snake")
snake = MySnake(400, 300, 4, screen, "snake.png", "snake.png")
font = pygame.font.Font(None, 26)
font1 = pygame.font.Font(None, 40)

game_over = False

rect_points = [(10, 30), (790, 30), (790, 590), (10, 590)]


def init_snake():
    snake.draw_snake()


def move_snake(keys):
    # 根据方向按键，调整行进方向
    direction = snake.direction

    if keys[K_UP]:
        direction = "up"
    elif keys[K_DOWN]:
        direction = "down"
    elif keys[K_LEFT]:
        direction = "left"
    elif keys[K_RIGHT]:
        direction = "right"

    if direction:
        snake.move(direction)


def draw_infos(score, time_last):
    img_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    screen.blit(img_text, (10, 10))

    img_text = font.render("Time: {}".format(time_last), True, (0, 0, 0))
    screen.blit(img_text, (410, 10))


def refresh_surface():
    # 白色填充
    screen.fill((255, 255, 255))

    # 画矩形框
    pygame.draw.lines(screen, (0, 0, 0), True, rect_points, 3)

    # 添加分数，时间
    draw_infos(0, 0)

    # 画snake
    snake.draw_snake()


def check_collide():
    return snake.check_collide_boundary() or snake.check_collide_snake()


def run_snake():
    while True:
        timer.tick(5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

        # 如果游戏结束，提示重启
        global game_over
        if game_over is not True:
            game_over = check_collide()
        else:
            img_text = font1.render("Press Space To Restart Game!", True, (0, 0, 0))
            screen.blit(img_text, (300, 300))
            pygame.display.update()

            # 如果game over状态下，按enter，重启游戏
            if keys[K_SPACE]:
                game_over = False
                global snake
                snake = MySnake(400, 300, 4, screen, "snake.png", "snake.png")

            continue

        # 计算snake下一步移动方向
        move_snake(keys)

        # 重绘图
        refresh_surface()

        # 刷新显示
        pygame.display.update()


if __name__ == "__main__":
    screen.fill((255, 255, 255))
    timer = pygame.time.Clock()

    init_snake()
    run_snake()
