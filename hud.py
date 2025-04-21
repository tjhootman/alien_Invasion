import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class HUD:
    """A class to manage and display the Heads-Up Display (HUD) information."""

    def __init__(self, game):
        """Initialize the hUD attributes.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
                Provides access to game settings, screen, and game statistics.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file,
            self.settings.HUD_font_size
            )
        # padding from the edges of the screen
        self.padding = 20
        # prepare the initial score display
        self.update_scores()
        # setup the image for displaying remaining lives
        self._setup_life_image()
        # prepare the initial level display
        self.update_level()

    def _setup_life_image(self):
        """Load and scale the image used to represent remaining lives."""
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        self.life_rect = self.life_image.get_rect()

    def update_scores(self):
        """Update the displayed score, maximum score, and high score."""
        self._update_max_score()
        self._update_score()
        self._update_hi_score()

    def _update_score(self):
        """Render the current score to an image and position it."""
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True,
            self.settings.text_color, None
            )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def _update_max_score(self):
        """Render the maximum score of the current game to an image and position it."""
        max_score_str = f'Max-Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True,
            self.settings.text_color, None
            )
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self):
        """Render the all-time high score to an image and position it at the top-center."""
        hi_score_str = f'Hi-Score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True,
            self.settings.text_color, None
            )
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self):
        """Render the current game level to an image and position it at the top-left."""
        level_str = f'Level: {self.game_stats.level: ,.0f}'
        self.level_image = self.font.render(level_str, True,
            self.settings.text_color, None
            )
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.life_rect.bottom + self.padding

    def _draw_lives(self):
        """Draw the remaining lives icons on the screen."""
        current_x = self.padding
        current_y = self.padding
        for i in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self):
        """Draw all HUD elements to the screen."""
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()
