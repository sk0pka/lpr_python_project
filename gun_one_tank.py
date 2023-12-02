import math

from random import randint, choice

import pygame
from pygame.locals import *
import pygame.font


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]
TARGET_COLORS = [GREY]

WIDTH = 800
HEIGHT = 600


def display_info(score, lives):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Points: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ball_type = choice(["normal", "special", "invisible"])
        self.live = 30
        self.r = 5
        self.gravity = -0.5
        self.color = choice(GAME_COLORS)

        if self.ball_type == "normal":
            self.color = choice(GAME_COLORS)
            self.r = 10
            self.gravity = -0.5
        elif self.ball_type == "special":
            self.color = BLACK
            self.r = 4
            self.gravity = 0.5
        elif self.ball_type == "invisible":
            self.color = WHITE
            self.r = 30
            self.gravity = -0.3

    def move(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y -= self.vy

        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            self.vx = -self.vx

        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy

        if self.y - self.r < 0:
            self.y = self.r
            self.vy = -self.vy

    def draw(self, xn, yn):
        self.x = xn
        self.y = yn
        pygame.draw.circle(
            self.screen,
            self.color,
            (xn, yn),
            self.r
        )

    def hittest(self, obj):
        distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
        return distance < (self.r + obj.r)


class Gun:
    def __init__(self, screen):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.width = 30
        self.height = 20
        self.speed = 5
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.lives = 55

    def lose_life(self):
        self.lives -= 1

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, tank_X, tank_Y)
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):

        if event:
            self.an = math.atan((event.pos[1]-tank_Y) / (event.pos[0]-tank_X))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + max(self.f2_power, 20) * math.cos(self.an),
            self.y + max(self.f2_power, 20) * math.sin(self.an),)
            ,7)
        pygame.draw.rect(screen, self.color, (self.x-self.width, self.y, self.width, self.height))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, a, b):
        self.live = 1
        self.speedx = a
        self.speedy = b
        self.new_target()
        self.bomb_cooldown = randint(50, 150)
        self.target_type = choice(["normal", "horizontal", "vertical"])
        self.color = choice(TARGET_COLORS)
        self.border_color = BLACK

        if self.target_type == "horizontal":
            self.speedy = 0
        elif self.target_type == "vertical":
            self.speedx = 0

    def new_target(self):
        self.target_type = choice(["normal", "horizontal", "vertical"])
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)

    def move(self):
        self.x += self.speedx
        self.y += self.speedy

        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            self.speedx = -self.speedx

        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.speedy = -self.speedy

        if self.y - self.r < 0:
            self.y = self.r
            self.speedy = -self.speedy

        self.bomb_cooldown -= 1
        if self.live and randint(0, 100) < 1:  # Adjust the probability as needed
            self.launch_bomb()

    def draw(self):
        if self.live:
            pygame.draw.circle(screen, self.border_color, (self.x, self.y), self.r)
            pygame.draw.circle(screen, self.color, (self.x, self.y), 0.95*self.r)

    def launch_bomb(self):
        if self.bomb_cooldown <= 0:
            bomb = Bomb(screen, self.x, self.y, tank_X, tank_Y)
            bombs.append(bomb)
            self.bomb_cooldown = randint(50, 150)


class Bomb:
    def __init__(self, screen: pygame.Surface, x, y, target_x, target_y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.speed = 5
        self.color = RED

        # Calculate the direction towards the tank
        angle = math.atan2(target_y - y, target_x - x)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def move(self):
        self.y += self.vy
        self.x += self.vx

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tank_X = WIDTH // 2
tank_Y = HEIGHT // 2
bullet = 0
score = 0

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target(0.6 * randint(1, 6), 0.5 * randint(1, 7)) for _ in range(3)]
finished = False
balls = []
bombs = []

while not finished:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    tank_X = gun.x
    tank_Y = gun.y
    if gun.lives <= 0:
        finished = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    gun.draw()
    gun.move(keys)

    for target in targets:
        target.draw()
        target.move()

        for bomb in bombs:
            bomb.move()
            bomb.draw()

            if (
                    hasattr(bomb, 'x') and  # Check if bomb has 'x' attribute
                    tank_X - gun.width / 2 < bomb.x < tank_X + gun.width / 2 and
                    tank_Y - gun.height < bomb.y < tank_Y + gun.height / 2
            ):
                gun.lose_life()
                bombs.remove(bomb)

    display_info(score, gun.lives)

    for b in balls:
        b.move()

    for target in targets:
        for b in balls:
            if b.hittest(target) and target.live:
                target.new_target()
                score += 1
                balls.remove(b)

    for b in balls:
        b.draw(b.x, b.y)

    gun.power_up()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()