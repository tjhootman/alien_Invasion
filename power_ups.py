import pygame
import random
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class PowerUps(Sprite):

    def __init__(self, game: 'AlienInvasion', x: float, y: float, power_up_type):
        super().__init__()

        self.game = game
        self.boundaries = self.game.screen.get_rect()
        self.settings = self.game.settings

        # load the power up image and scale it.
        self.image = pygame.image.load(self.settings.power_up_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.power_up_w, self.settings.power_up_h)
            )

        # create the power up rect object, position it and set drop speed.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = game.settings.power_up_drop_speed
        self.power_up_type = power_up_type
        