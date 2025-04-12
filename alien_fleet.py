import pygame
from typing import TYPE_CHECKING
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """Manages the creation, movement and destruction of the alien fleet.
    """
    def __init__(self, game: 'AlienInvasion'):
        """Initializes the AlienFleet.

        Args:
            game (AlienInvasion): A reference to the main AlienInvasion game instance.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """Creates the initial alien fleet."""
        alien_h = self.settings.alien_h
        alien_w = self.settings.alien_w
        screen_h = self.settings.screen_h
        screen_w = self.settings.screen_w

        fleet_h, fleet_w = self.calculate_fleet_size(alien_h, screen_h, alien_w, screen_w)
        y_offset, x_offset = self.calculate_offsets(alien_h, alien_w, screen_h, fleet_h, fleet_w)
        
        self._create_rectangle_fleet(alien_h, alien_w, fleet_h, fleet_w, y_offset, x_offset)

    def _create_rectangle_fleet(self, alien_h, alien_w, fleet_h, fleet_w, y_offset, x_offset):
        """Creates a rectangular formation of aliens.

        Args:
            alien_h (int): The height of a single alien.
            alien_w (int): The width of a single alien.
            fleet_h (int): The height of the fleet.
            fleet_w (int): The width of the fleet.
            y_offset (int): The vertical offset for the start of the fleet.
            x_offset (int): The horizontal offset for the start of the fleet.
        """
        for row in range(fleet_w):
            for col in range(fleet_h):
                current_y = alien_h * col + y_offset
                current_x = alien_w * row + x_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_h, alien_w, screen_h, fleet_h, fleet_w):
        """Calculates the vertical and horizontal offsets to center the fleet.

        Args:
            alien_h (int): The height of a single alien.
            alien_w (int): The width of a single alien.
            screen_h (int): The height of the game screen.
            fleet_h (int): The height of the fleet.
            fleet_w (int): The width of the fleet.

        Returns:
            tuple: A tuple containing the vertical (y) and horizontal (x) offsets.
        """
        half_screen = self.settings.screen_w // 2
        fleet_vertical_space = fleet_h * alien_h
        fleet_horizontal_space = fleet_w * alien_w
        y_offset = int((screen_h - fleet_vertical_space) // 2)
        x_offset = int((half_screen + fleet_horizontal_space) // 2)
        return y_offset,x_offset

    def calculate_fleet_size(self, alien_h, screen_h, alien_w, screen_w):
        """Calculates the ideal dimensions (height and width in number of aliens)
        for the alien fleet based on alien size and screen dimensions.

        Args:
            alien_h (int): The height of a single alien.
            screen_h (int): The height of the game screen.
            alien_w (int): The width of a single alien.
            screen_w (int): The width of the game screen.

        Returns:
            tuple: A tuple containing the calculated fleet height and width.
        """
        fleet_h = (screen_h // alien_h)
        fleet_w = ((screen_w / 2) // alien_w)

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        
        if fleet_w % 2 == 0:
            fleet_w -= 2
        else:
            fleet_w -= 1

        return int(fleet_h), int(fleet_w)
    
    def _create_alien(self, current_x:int, current_y:int):
        """Creates a single alien at the specified coordinates and adds it to the fleet.

        Args:
            current_x (int): The hoizontal position for the new alien.
            current_y (int): The veritcal position for the new alien.
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Checks if any alien in the fleet has reached the left or right edges 
        of the screen. If so, it calls the method to drop the fleet and change 
        its horizontal direction.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
        
    def _drop_alien_fleet(self):
        """Drops the entire alien fleet down the screen by the fleet's drop speed.
        """
        for alien in self.fleet:
            alien.x += self.fleet_drop_speed

    def update_fleet(self):
        """Updates the position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """Draws all aliens in the fleet on the screen.
        """
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Checks for collisions between the alien fleet and another sprite group.

        Args:
            other_group: A pygame.sprite.Group object to check for collisions with.

        Returns:
            dict: A dictionary containing the sprites that collided. The keys are the
            sprites in the 'fleet' that collided, and the values are lists of the
            sprites in 'other_group' that they collided with. Returns an empty
            dictionary if no collisions occur.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        """Checks if any alien in the fleet has reached the bottom edge of the screen.

        Returns:
            bool: True if any alien's bottom edge is at or below the screen's 
            bottom edge. False otherwise.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False
    
    def check_destroyed_status(self):
        """Checks if the alien fleet is empty (all aliens have been destroyed).

        Returns:
            bool: True if the fleet is empty, False otherwise.
        """
        return not self.fleet
    