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

    def collision(self):
        if pygame.sprite.spritecollide(self, enemies, True):
            remove_all_sprites()
            global GAMESTATE
            GAMESTATE = 2

    def update(self, *args, **kwargs):
        self.player_input()
        self.collision()


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load("assets/enemy/1/enemy1.webp").convert_alpha()
        image = pygame.transform.flip(image, False, True)
        self.image = pygame.transform.smoothscale(image, (76, 120))
        self.rect = self.image.get_frect(topleft=(x, y))

    def update(self, *args, **kwargs):
        self.rect.y += 0.2

    def move(self):
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, midbottom):
        super().__init__()
        self.image = pygame.image.load("assets/bullet/bullet.webp").convert_alpha()
        self.rect = self.image.get_rect(midbottom=midbottom)

    def collision(self):
        if pygame.sprite.spritecollide(self, enemies, True) or self.rect.top <= 0:
            self.kill()
            if len(enemies) == 0:
                remove_all_sprites()
                global GAMESTATE
                GAMESTATE = 3

    def update(self, *args, **kwargs):
        self.rect.y -= 1.5
        self.collision()


def start():
    global player
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    global enemies
    enemies = pygame.sprite.Group()
    for y in range(20, 381, 120):
        for x in range(40, SCREENSIZE[0] - 76 - 39, 86):
            enemies.add(Enemy(x, y))

    global bullets
    bullets = pygame.sprite.Group()


def remove_all_sprites():
    player.empty()
    enemies.empty()
    bullets.empty()


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Space game")
clock = pygame.time.Clock()

logo = pygame.image.load("assets/logo.webp").convert_alpha()
logorect = logo.get_rect(topleft=(80, 200))
start_btn = pygame.image.load("assets/start.png").convert_alpha()
start_btn_rect = start_btn.get_rect(center=(SCREENSIZE[0] // 2, 600))

LARGE_FONT = pygame.font.Font("assets/Sixtyfour-Regular.ttf", 40)
gameover_text = LARGE_FONT.render("Game over!", True, (255, 255, 255))
gameover_rect = gameover_text.get_rect(center=(SCREENSIZE[0] // 2, 300))

win_text = LARGE_FONT.render("You won!", True, (255, 255, 255))
win_rect = win_text.get_rect(center=(SCREENSIZE[0] // 2, 300))


GAMESTATE = 0
# 0 = startscreen
# 1 = game
# 2 = game over
# 3 = win

stars = [Star() for _ in range(500)]



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if GAMESTATE in (0, 2, 3):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_btn_rect.collidepoint(pygame.mouse.get_pos()):
                GAMESTATE = 1
                start()
        elif GAMESTATE == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(bullets) == 0:
                        bullets.add(Bullet(player.sprite.rect.midtop))

    screen.fill((0, 0, 0))

    for star in stars:
        pygame.draw.circle(screen, (star.color, star.color, star.color), (star.x, star.y), star.radius)
        star.update()

    if GAMESTATE == 0:
        screen.blit(logo, logorect)
        screen.blit(start_btn, start_btn_rect)
    elif GAMESTATE == 1:
        enemies.update()
        enemies.draw(screen)

        bullets.update()
        bullets.draw(screen)

        player.update()
        player.draw(screen)
    elif GAMESTATE == 2:
        screen.blit(gameover_text, gameover_rect)
        screen.blit(start_btn, start_btn_rect)
    elif GAMESTATE == 3:
        screen.blit(win_text, win_rect)
        screen.blit(start_btn, start_btn_rect)

    pygame.display.update()
    clock.tick(60)
