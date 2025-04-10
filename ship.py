import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """Creates a ship and manages its movement and firing capabilities. """
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Initialize the ship and set its starting postion. 

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
            This provides access to game resources like settings.
            arsenal (Arsenal): An instance of the Arsenal class, responsible for
            firing the ship's bullets.
        """
        # store references to the game and settings
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        # get the screen's rectangular boundaries
        self.boundaries = self.screen.get_rect()

        # load the ship image, scale and rotate it according to the settings
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        self.image = pygame.transform.rotate(self.image, self.settings.ship_rotate)

        # get the rectangular area of the ship image and set it's inital position
        self.rect = self.image.get_rect()
        self.rect.midleft = self.boundaries.midleft

        # movement flags to track if ship is moving up or down
        self.moving_down = False
        self.moving_up = False

        # store the ship's vertical position
        self.y = float(self.rect.y)

        # store a reference to the ship's arsenal
        self.arsenal = arsenal

    def update(self):
        """Update the ship's position and the arsenal of bullets."""
        # update the ship's vertical movement
        self._update_ship_movement()
        # update the state and position of the bullets in the arsenal
        self.arsenal.update_aresenal()

    def _update_ship_movement(self):
        """Update the ship's vertical position."""
        temp_speed = self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed

        # update the ship's y-coordinates
        self.rect.y = self.y

    def draw(self):
        """Draw the ship its arsenal of bullets on screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Tell the arsenal to fire a new bullet if possible.
        Returns:
            bool_: True if a bullet was fired, False otherwise (if the bullet
            limit was reached).
        """
        return self.arsenal.fire_bullet()
