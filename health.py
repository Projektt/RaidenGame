import pygame
from pygame.sprite import Sprite

class Health(Sprite):
    """A class to manage the HP Bar."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the HP image and get its rect.
        self.image = pygame.image.load('images/health.bmp')
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)