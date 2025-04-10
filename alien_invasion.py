import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal

class AlienInvasion:
    """Class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

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

        # create the ship and its aresnal of bullets
        self.ship = Ship(self, Arsenal(self))

    def run_game(self):
        """Start the main game loop."""
        while self.running:
            # check for user input and events
            self._check_events()
            # update the ship's position
            self.ship.update()
            # update the display to show latest changes
            self._update_screen()
            # limit the frame rate of the game
            self.clock.tick(self.settings.FPS)

    def _update_screen(self):
        """Update the images on the screen and flip to new screen."""
        # draw the background 
        self.screen.blit(self.bg, (0,0))
        # draw the ship
        self.ship.draw()
        # make most recent screen draw visible
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
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
            pygame.quit()
            sys.exit()
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
