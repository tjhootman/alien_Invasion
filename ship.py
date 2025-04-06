import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        # initial ship settings
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        self.image = pygame.transform.rotate(self.image, self.settings.ship_rotate)

        self.rect = self.image.get_rect()
        self.rect.midleft = self.boundaries.midleft
        self.moving_right = False
        self.moving_left = False
        self.y = float(self.rect.y)
        self.arsenal = arsenal

    def update(self):
        # updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_aresenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        if self.moving_left and self.rect.top > self.boundaries.top:
            self.y -= temp_speed

        self.rect.y = self.y

    def draw(self):
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        return self.arsenal.fire_bullet()