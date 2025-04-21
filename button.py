import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """A class to create interactive buttons in the game."""

    def __init__(self, game: 'AlienInvasion', msg):
        """Initialize button attributes. 

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
                Provides access to game settings and the screen.
            msg (str): The text to be displayed on the button.
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file,
            self.settings.button_font_size
            )
        # create the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        # prepare the button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Render the message into an image and center it on the button.

        Args:
            msg (str): The text to be displayed on the button.
        """
        # render the message with the specified font, color, and background
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        # get the rect of the rendered message image
        self.msg_image_rect = self.msg_image.get_rect()
        # center the message image on the button rect
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button to the screen."""
        # fill the button's rectangle with the button color
        self.screen.fill(self.settings.button_color, self.rect)
        # blit the message image onto the screen at its center
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """Check if the mouse click position is within the button's boundaries.

        Args:
            mouse_pos (tuple): The (x,y) coordinates of the mouse click.

        Returns:
            bool: True if the mouse click collided with button's rectangle,
                False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)
