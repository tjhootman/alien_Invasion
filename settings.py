from pathlib import Path

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # game settings
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        # ship settings
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        self.ship_rotate = -90

        # bullet settings
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserGreen.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        self.bullet_rotate = -90

        # alien settings
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40
        self.alien_rotate = -90
        self.fleet_direction = 1

        # button settings
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)
        self.text_color = (255,255,255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 5
        self.staring_ship_count = 3

        self.bullet_speed = 7
        self.bullet_amount = 6
        self.bullet_w = 25
        self.bullet_h = 80

        self.fleet_speed = 2
        self.fleet_drop_speed = -40
        self.alien_points = 50

    def increase_difficulty(self):
        """Inscrease the speed of game elements."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale
        self.fleet_drop_speed *= self.difficulty_scale
