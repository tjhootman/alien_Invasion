import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
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
        # create an instance to store game statistics
        self.game_stats = GameStats(self)
        # create and instance for the Heads-Up Display
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
        
        # create the play button
        self.play_button = Button(self, 'Play')
        # flag to indicate if the game is currently active
        self.game_active = False

    def run_game(self):
        """Start the main game loop."""
        pygame.mixer.init()
        # load the background music
        pygame.mixer.music.load(self.settings.bg_music)
        # set the volume of the background music
        pygame.mixer.music.set_volume(0.5)
        # play background music
        pygame.mixer.music.play(-1)
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
            # Initialize the mixer
            
    def _check_collisions(self):
        """Check for collisions between game elements."""
        # check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
           self._check_game_status()

       # check if alien has reached the bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

        # check for collisions between bullets and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        #check if the entire alien fleet has been destroyed
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
            # decrement the number of ships left
            self.game_stats.ships_left -= 1
            # reset the game level
            self._reset_level()
            # pause briefly to allow the player to see consequence
            sleep(0.5)
        else:
            # set the game to inactive when no ships are left
            self.game_active = False
        
    def _reset_level(self):
        """Resets the game level by clearing existing projectiles and aliens,
        and then creates a new alien fleet.
        """
        # remove all existing bullets
        self.ship.arsenal.arsenal.empty()
        # remove all existing aliens
        self.alien_fleet.fleet.empty()
        # create a new fleet of aliens
        self.alien_fleet.create_fleet()

    def restart_game(self):
        """Restarts the game by resetting settings, statistics, and game of elements."""
        # re-initialize dynamice game settings
        self.settings.initialize_dynamic_settings()
        # reset game statistics
        self.game_stats.reset_stats()
        # update the score to displat on HUD
        self.HUD.update_scores()
        # reset the game level
        self._reset_level()
        # center the player's ship
        self.ship._center_ship()
        # set the game to active
        self.game_active = True
        # hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update the images on the screen and flip to new screen."""
        # draw the background 
        self.screen.blit(self.bg, (0,0))
        # draw the ship
        self.ship.draw()
        # draw the alien fleet
        self.alien_fleet.draw()
        # draw the Heads-Up Display
        self.HUD.draw()

        # draw the play button if the game is not active
        if not self.game_active:
            self.play_button.draw()
            # make the mouse cursor visible
            pygame.mouse.set_visible(True)

        # make most recent screen draw visible
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # set the running flag to False to exit the game loop
                self.running = False
                # save the high scores before quitting
                self.game_stats.save_scores()
                # uninitialize all pygame modules
                pygame.quit()
                # exit the game
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                # check for key presses if the game is active
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # check for key releases
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check for mouse button clicks
                self._check_button_clicked()

    def _check_button_clicked(self):
        # get the current position of the mouse
        mouse_pos = pygame.mouse.get_pos()
        # check if the mouse click is within the bounds of the play button
        if self.play_button.check_clicked(mouse_pos):
            # start a new game if the play button is clicked
            self.restart_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_DOWN:
            # stop if moving down when the down arrow key is released
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            # stop moving up when the up arrow key is released
            self.ship.moving_up = False
        
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_DOWN:
            # start moving down when the down arrow key is pressed
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            # start moving up when the up arrow key is pressed
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            # fire a bullet and play laser sound if possible
            if self.ship.fire():
                self.laser_sound.play()
                # fade out the laser sound
                self.laser_sound.fadeout(500)
        elif event.key == pygame.K_q:
            # quit game if the 'q' key is pressed
            self.running = False
            # save the high scores before quitting
            self.game_stats.save_scores()
            # uninitialize all pygame modules
            pygame.quit()
            # exit the system
            sys.exit()
            
if __name__ == '__main__':
    # create an instance of the AlienInvasion Game
    ai = AlienInvasion()
    # run the main game loop
    ai.run_game()
