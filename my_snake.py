import random

import pygame
# from pygame.locals import *


const_scale = 15
food_scale = 18


class MySnake(object):
    def __init__(self, head_x, head_y, snake_len, screen, img_snake_body, img_food, direction="right"):
        self.head_x = head_x
        self.head_y = head_y

        self.img_snake_body = pygame.image.load(img_snake_body)
        w, h = self.img_snake_body.get_size()
        self.img_snake_body = pygame.transform.smoothscale(self.img_snake_body, (w // const_scale, h // const_scale))
        self.img_snake_body_w, self.img_snake_body_h = w // const_scale, h // const_scale

        self.img_food = pygame.image.load(img_food)
        w, h = self.img_food.get_size()
        self.img_food = pygame.transform.smoothscale(self.img_food, (w // food_scale, h // food_scale))

        self.snake = []
        for i in range(snake_len):
            self.snake.append({"x": self.head_x - (i * self.img_snake_body_w), "y": self.head_y})

        self.direction = direction
        self.screen = screen

        self.food_position = None
        self.generate_food()

    def generate_food(self):
        self.food_position = random.randint(10, 780) * 10 // 10, random.randint(30, 580) * 10 // 10

    def move(self, direction):
        # 根据按键移动方向，与snake当前移动方向比较，如果方向相逆，则忽略本次按键方向，继续按当前方向行进
        if direction == "right":
            if self.direction == "left":
                direction = "left"
        elif direction == "down":
            if self.direction == "up":
                direction = "up"
        elif direction == "left":
            if self.direction == "right":
                direction = "right"
        elif direction == "up":
            if self.direction == "down":
                direction = "down"
        else:
            return

        # 根据行进方向就算snake head的下一次的行进位置
        if direction == "right":
            self.direction = direction
            head_position = self.snake[0]["x"] + self.img_snake_body_w, self.snake[0]["y"]
        elif direction == "down":
            self.direction = direction
            head_position = self.snake[0]["x"], self.snake[0]["y"] + self.img_snake_body_h
        elif direction == "left":
            self.direction = direction
            head_position = self.snake[0]["x"] - self.img_snake_body_w, self.snake[0]["y"]
        elif direction == "up":
            self.direction = direction
            head_position = self.snake[0]["x"], self.snake[0]["y"] - self.img_snake_body_h
        else:
            return

        # 逆序遍历snake每一节数据，后一节body的下一个位置就是上一节body的当前位置，遍历到snake head
        for snake_body_idx in range(len(self.snake) - 1, 0, -1):
            self.snake[snake_body_idx]["x"] = self.snake[snake_body_idx - 1]["x"]
            self.snake[snake_body_idx]["y"] = self.snake[snake_body_idx - 1]["y"]

        # 设置snake head位置
        self.snake[0]["x"] = head_position[0]
        self.snake[0]["y"] = head_position[1]

    def enhance_snake_body(self):
        for _ in self.snake[:0:-1]:
            self.snake.append({"x": self.snake[:-1]["x"] + self.img_snake_body_w, "y": self.snake[:-1]["y"]})

    def draw_snake(self):
        # 绘制food
        self.screen.blit(self.img_food, (self.food_position[0], self.food_position[1]))

        # 在屏幕上绘制整个snake
        for snake_body in self.snake:
            self.screen.blit(self.img_snake_body, (snake_body["x"], snake_body["y"]))

    def check_collide_snake(self):
        for one_snake in self.snake[1:]:
            if self.snake[0]["x"] == one_snake["x"] and self.snake[0]["y"] == one_snake["y"]:
                return True

        return False

    def check_collide_boundary(self):
        if self.snake[0]["x"] < 40 or self.snake[0]["x"] > 750:
            return True

        if self.snake[0]["y"] < 50 or self.snake[0]["y"] > 550:
            return True

        return False
