import random
import sys

import pygame


SCREENSIZE = (500, 800)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player/1/base.webp").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(SCREENSIZE[0] / 2, SCREENSIZE[1] - 20))
        self.last_shoot = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        SPEED = 8
        if keys[pygame.K_RIGHT] and self.rect.right < SCREENSIZE[0] - 40:
            self.rect.x += min(SPEED, SCREENSIZE[0] - self.rect.right)
        elif keys[pygame.K_LEFT] and self.rect.left > 40:
            self.rect.x -= min(SPEED, self.rect.left - 40)

    def update(self, *args, **kwargs):
        self.player_input()


class Star:
    def __init__(self):
        self.x = random.randint(0, SCREENSIZE[0])
        self.y = random.uniform(-10, SCREENSIZE[1])
        self.radius = random.randint(1, 2)
        if self.radius == 1:
            self.color = random.randint(200, 255)
            self.speed = random.uniform(0.2, 0.6)
        else:
            self.color = 255
            self.speed = random.uniform(0.4, 0.8)


    def update(self):
        self.y += self.speed
        if self.y > SCREENSIZE[1] + 10:
            self.y = -10


pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Space game")
clock = pygame.time.Clock()


player = pygame.sprite.GroupSingle()
player.add(Player())


stars = [Star() for _ in range(500)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("shoot")

    screen.fill((0, 0, 0))

    for star in stars:
        pygame.draw.circle(screen, (star.color, star.color, star.color), (star.x, star.y), star.radius)
        star.update()

    player.update()
    player.draw(screen)
    pygame.display.update()

    clock.tick(60)
