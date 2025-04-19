import pygame
import random
from pathlib import Path
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet
    from pathlib import Path
    import random

class Alien(Sprite):
    """A class to manage aliens."""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Create a alien object and set it's screen position.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
            This provides access to game resources like settings.
        """
        super().__init__()

        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        # load the alien image, scale and rotate it.
        self.alien_images = self.settings.alien_images
        self.image = pygame.image.load(Path.cwd() / 'Assets' / 'images' / (random.choice(self.alien_images)))
        # self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        self.image = pygame.transform.rotate(self.image, self.settings.alien_rotate)

        # create the aliens rect object and position it.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the alien's vertical position."""
        temp_speed = self.settings.fleet_speed

        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.y = self.y
        self.rect.x = self.x

    def check_edges(self):
        """Checks if the sprite's top or bottom edge has gone beyond the defined 
        boundaries.

        Returns:
            bool: True if the bottom edge of the sprite's rectangle is greater 
            than or equal to the bottom boundary, or if the top edge of the 
            sprite's rectangle is less than or equal to the top boundary. 
            False otherwise.
        """
        return (
            self.rect.bottom >= self.boundaries.bottom 
            or self.rect.top <= self.boundaries.top
            )

    def draw_alien(self):
        """Draw the alien to the screen."""
        self.screen.blit(self.image, self.rect)
