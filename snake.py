import pygame
import sys
from pygame.locals import *

from my_snake import MySnake

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("snake")
snake = MySnake(400, 300, 4, screen, "snake.png", "snake.png")
font = pygame.font.Font("simhei.ttf", 18)
font1 = pygame.font.Font("simhei.ttf", 30)

game_over = False
game_score = 0
game_level = 1
rect_points = [(10, 30), (790, 30), (790, 590), (10, 590)]


def init_snake():
    snake.draw_snake()
    pygame.display.update()


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
        return snake.move(direction)


def draw_infos(score, time_last):
    img_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    screen.blit(img_text, (10, 10))

    img_text = font.render("Level: {}".format(time_last), True, (0, 0, 0))
    screen.blit(img_text, (410, 10))

    img_text = font.render("x = {}, y = {}".format(snake.snake[0]["x"], snake.snake[0]["y"]), True, (0, 0, 0))
    screen.blit(img_text, (610, 10))


def refresh_surface():
    # 白色填充
    screen.fill((255, 255, 255))

    # 画矩形框
    pygame.draw.lines(screen, (0, 0, 0), True, rect_points, 3)

    # 添加分数，时间
    draw_infos(game_score, game_level)

    # 画snake
    snake.draw_snake()


def check_collide():
    return snake.check_collide_snake()


def check_snake_food():
    return snake.check_snake_food()


def upgrade_game_level():
    global game_level
    if game_score < 100:
        game_level = 1
    elif game_score < 200:
        game_level = 2
    elif game_score < 300:
        game_level = 3
    elif game_score < 400:
        game_level = 4
    elif game_score < 500:
        game_level = 5
    elif game_score < 600:
        game_level = 6
    elif game_score < 700:
        game_level = 7
    elif game_score < 800:
        game_level = 8
    else:
        game_level = 9


def run_snake():
    while True:
        global game_level, game_score, game_over
        timer.tick(game_level * 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

        # 计算snake下一步移动方向
        if game_over is not True:
            game_over = move_snake(keys)

        # 如果游戏结束，提示重启
        if game_over is not True:
            game_over = check_collide()
        else:
            img_text = font1.render("Press Space To Restart Game!", True, (0, 0, 0))
            screen.blit(img_text, (200, 200))
            draw_infos(game_score, game_level)
            pygame.display.update()

            # 如果game over状态下，按enter，重启游戏
            if keys[K_SPACE]:
                game_over = False
                global snake
                snake = MySnake(400, 300, 4, screen, "snake.png", "snake.png")
                game_level = 1
                game_score = 0

            continue

        # 判断吃到food
        if check_snake_food():
            game_score += 10
            # 速度升级
            upgrade_game_level()

        # 重绘图
        refresh_surface()

        # 刷新显示
        pygame.display.update()


if __name__ == "__main__":
    screen.fill((255, 255, 255))
    timer = pygame.time.Clock()

    init_snake()
    run_snake()
