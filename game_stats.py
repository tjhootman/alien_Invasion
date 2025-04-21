import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """Tracks statistics for the game."""

    def __init__(self, game: 'AlienInvasion'):
        """Initialize game statistics.

        Args:
            game (AlienInvasion): An instance of the AlienInvasion game class.
                Provides access to game settings and file paths. 
        """
        self.game = game
        self.settings = game.settings
        # initialize the maximum score for the current game
        self.max_score = 0
        # initialize high scores from saved data
        self.init_saved_scores()
        # reset the game statistics for a new game
        self.reset_stats()

    def init_saved_scores(self):
        """Initialize the high score from a JSON file if it exists and has content."""
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()

    def save_scores(self):
        """Save the current high score to a JSON file."""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not FoundL {e}')

    def reset_stats(self):
        """Reset game statistics that can change during the game."""
        self.ships_left = self.settings.staring_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """Update game statistics based on game events.

        Args:
            collisions (dict): A dictionary representing collisions between aliens
                and bullets. The keys are the aliens that were hit.
        """
        # update the current score based on collisions
        self._update_score(collisions)
    
        #update the maximum score for the current game
        self._update_max_score()

        # update the overall high score
        self.update_hi_score()

    def _update_max_score(self):
        """Update the maximum score achieved in the current game."""
        if self.score > self.max_score:
            self.max_score = self.score

    def update_hi_score(self):
        """Update the overall high score if the current score is higher."""
        if self.score > self.hi_score:
            self.hi_score = self.score

    def _update_score(self, collisions):
        """Update the current game score based on the number of aliens hit.

        Args:
            collisions (dict): A dictionary where keys are the aliens that were hit.
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points

    def update_level(self):
        """Increase the game level by one."""
        self.level += 1
