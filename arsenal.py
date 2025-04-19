import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """A class to manage the arsenal of bullets fired by the ship."""

    def __init__(self, game: 'AlienInvasion'):
        """Initialize the arsenal and create an empty group to store bullets.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
            This provides access to game resources like settings.
        """
        self.game = game
        self.settings = game.settings
        # create and empty group to store bullets
        self.arsenal = pygame.sprite.Group()

    def update_aresenal(self):
        """Update the position of each bullet in the arsenal and remove
        off-screen bullets."""
        # update he position of all bullets in the group
        self.arsenal.update()
        # remove bullets that have moved off-screen
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """Remove bullets that have moved past the right edge of the screen."""
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.settings.screen_w:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw all bullets in the arsenal to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        """Create a new bullet and add it to the arsenal if the limit is not reached.

        Returns:
            bool: True if a new bullet was fired, False otherwise (if the bullet
            limit was reached).
        """
        # check if the number of bullets is less than the allowed amount.
        if len(self.arsenal) < self.settings.bullet_amount:
            # create a new bullet object
            new_bullet = Bullet(self.game)
            # add the new bullet to the arsenal group.
            self.arsenal.add(new_bullet)
            return True
        return False
    
    def fire_spread_shot(self):
        bullet1 = Bullet(self.game)
        bullet2 = Bullet(self.game, angle = -45)
        bullet3 = Bullet(self.game, angle = 45)
        self.bullets.add(bullet1)
        self.bullets.add(bullet2)
        self.bullets.add(bullet3)