import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game: 'AlienInvasion'):
        """Create a bullet object at the ship's current position.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
            This provides access to game resources like settings.
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # load the bullet image, scale and rotate it.
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_w, self.settings.bullet_h)
            )
        self.image = pygame.transform.rotate(self.image, self.settings.bullet_rotate)

        # create the bullets rect object and position it at the ships middle-right.
        self.rect = self.image.get_rect()
        self.rect.midright = game.ship.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet to the right of the screen."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
