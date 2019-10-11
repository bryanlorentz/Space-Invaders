import pygame
from pygame.sprite import Sprite


def load_image(name):
    image = pygame.image.load(name)
    return image


class Barrier(Sprite):
    def __init__(self, ai_settings, screen):
        super(Barrier, self).__init__()
        self.images = []
        self.screen = screen
        self.ai_settings = ai_settings
        self.images.append(load_image('images/barrier.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 100, 100)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        self.rect.x = self.x

        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def blitme(self):
        self.screen.blit(self.image, self.rect)