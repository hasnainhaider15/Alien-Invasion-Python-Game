import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A Class to re[resent sing;e alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien and specifies it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        """load the alien image and set it's rect atribute"""
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        """Start each new alien near the top left of the screen"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """Store the alie's exact horizontal position"""
        self.x = float(self.rect.x)

    def update(self):
        """Move the Aliens to right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at the eedge of the sceen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True 