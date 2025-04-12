import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """A class to manage aliens."""

    def __init__(self, game: 'AlienInvasion', x: float, y: float):
        """Create a alien object and set it's screen position.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
            This provides access to game resources like settings.
        """
        super().__init__()

        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings

        # load the alien image, scale and rotate it.
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        self.image = pygame.transform.rotate(self.image, self.settings.bullet_rotate)

        # create the aliens rect object and position it.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.x = float(self.rect.x)

    def update(self):
        pass

    def draw_alien(self):
        """Draw the alien to the screen."""
        self.screen.blit(self.image, self.rect)
