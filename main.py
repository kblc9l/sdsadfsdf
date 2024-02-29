import os
import sys
import random

import pygame

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


FRAMES_PER_SECOND = 50
clock = pygame.time.Clock()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()


class Bomb(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bomb.png"), (50, 50))
    image_boom = pygame.transform.scale(load_image("boom.png"), (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 100)
        self.rect.y = random.randrange(height - 100)
        self.mask = pygame.mask.from_surface(self.image)
        while True:
            f = True
            self.rect.x = random.randrange(width - 100)
            self.rect.y = random.randrange(height - 100)
            for b in bombs:
                if pygame.sprite.collide_mask(self, b):
                    f = False
                    break
            if f:
                break

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


bombs = []
for _ in range(20):
    bombs.append(Bomb(all_sprites))

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                all_sprites.update(event)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    clock.tick(50)

    pygame.display.flip()

pygame.quit()