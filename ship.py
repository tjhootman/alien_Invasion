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

        # get the rectangular area of the ship image
        self.rect = self.image.get_rect()

        ## set ship's initial position
        self.rect.midleft = self.boundaries.midleft

        # set ship's initial position
        self._center_ship()

        # movement flags to track if ship is moving up or down
        self.moving_down = False
        self.moving_up = False

        # store a reference to the ship's arsenal
        self.arsenal = arsenal

        # speed factor
        self.speed_factor = 1

        # flag for spread shot
        self.spread_shot_active = False

    def _center_ship(self):
        """Set ship's inital postion"""
        self.rect.midleft = self.boundaries.midleft
        self.y = float(self.rect.y)

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

    def check_collisions(self, other_group):
        """Checks for collisions between the calling sprite group and another 
        sprite group. If a collision occurs, the calling sprite is recentered.

        Args:
            other_group: A pygame.sprite.Group object to check for collisions with.

        Returns:
            bool: True if a collision occurs between any sprite in the calling group and
        any sprite in the 'other_group', False otherwise.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
