import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:
    """Class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        
        # set the display window size
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        # set the title of the game window
        pygame.display.set_caption(self.settings.name)

        # load the background image and scale it to the screen size
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h)
            )
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        # flag to indicate if game is running
        self.running = True
        # pygame clock to control the frame rate
        self.clock = pygame.time.Clock()

        # initialize the mixer module for sound
        pygame.mixer.init()
        # load the laser sound effect
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        # set the volume of the laser sound
        self.laser_sound.set_volume(0.7)
        # load the impact sound effect
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        # set the volume of the impact sound
        self.impact_sound.set_volume(0.7)

        # create the ship and its arsenal of bullets
        self.ship = Ship(self, Arsenal(self))
        # create the alien fleet
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        
        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self):
        """Start the main game loop."""
        while self.running:
            # check for user input and events
            self._check_events()
            if self.game_active:
                # update the ship's position
                self.ship.update()
                # update the fleet's position
                self.alien_fleet.update_fleet()
                # check for collisions
                self._check_collisions()
            # update the display to show latest changes
            self._update_screen()
            # limit the frame rate of the game
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        # check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
           self._check_game_status()
           
           # subtract one life if possible

       # check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        # check collisions of bullets and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            # update game stats level
            self.game_stats.update_level()
            # update HUD view
            self.HUD.update_level()

    def _check_game_status(self):
        """Checks the game status and performs actions based on the number of 
        ships left. If there are still ships remaining, it decrements the ship 
        count, resets the game level, and pauses briefly. If no ships are left, 
        it sets the game to inactive.
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
        
    def _reset_level(self):
        """Resets the game level by clearing existing projectiles and aliens,
        and then creates a new alien fleet.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update the images on the screen and flip to new screen."""
        # draw the background 
        self.screen.blit(self.bg, (0,0))
        # draw the ship
        self.ship.draw()
        # draw the alien fleet
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        # make most recent screen draw visible
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            # fire a bullet and play laser sound if possible
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            # quit game if the 'q' key is pressed
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
