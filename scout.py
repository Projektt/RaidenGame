
import pygame
import random
from pygame.sprite import Sprite

WIDTH = 1200
HEIGHT = 800

score = 0

class Scout(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_scout.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(1400, 1500)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        #Move the scout to the right.
        self.x -= self.settings.scout_speed
        self.rect.x = self.x
