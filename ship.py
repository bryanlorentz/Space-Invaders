import pygame
from pygame.sprite import Sprite


def load_image(name):
    image = pygame.image.load(name)
    return image


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.images = []
        self.screen = screen
        self.ai_settings = ai_settings
        self.images.append(load_image('images/ship1.png'))
        self.images.append(load_image('images/ship2.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 100, 100)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Explosion(Sprite):
    def __init__(self, ai_settings, screen):
        super(Explosion, self).__init__()
        self.images = []
        self.images.append(load_image('images/explosion1.png'))
        self.images.append(load_image('images/explosion2.png'))
        self.images.append(load_image('images/explosion3.png'))
        self.images.append(load_image('images/explosion4.png'))
        self.images.append(load_image('images/explosion5.png'))
        self.images.append(load_image('images/explosion6.png'))
        self.screen = screen
        self.ai_settings = ai_settings
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 100, 100)
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)