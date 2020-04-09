#import import_ipynb
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        
        # Creating the instance of Setting Class.
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """Old Code for small window of 1200 * 800 pixels"""
        #self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width, self.settings.screen_height))
        """Till Here"""
        
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game stats
        self.stats = GameStats(self)

        #instance of scoreboard
        self.sb = ScoreBoard(self)

        
        # Creating the instance of Ship Class.
        self.ship = Ship(self)

        #Creating bullet group to store cordia=nates of the bullet
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
         
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  #function call for event check

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen() # function call for update screen

    def _check_events(self):
        """Respond to keypress and mouse events"""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)        
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
               
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            """Reset game settings to the original"""
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True 
            """Reseting scoreboard on new game"""
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            """Get rid of any remaining aliens and bullets"""
            self.aliens.empty()
            self. bullets.empty()

            """Create the new fleet and center the ship"""
            self._create_fleet()
            self.ship.center_ship()

            """hide the mouse cursor"""
            pygame.mouse.set_visible(False)
   
    def _check_keydown_events(self, event):
        """Respond to kepress events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True             
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to keyrelease events"""
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update Position of bullets"""
        self.bullets.update()

        """ and get rid of old bullets"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check for any bullets that hit the aliens
            if so, get rif of the bullet anf the alien"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            """Destroy existing bullets and create new fleet"""
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            """Increase level"""
            self.stats.level +=1
            self.sb.prep_level()
    
    def _update_aliens(self):
        """check if the fleet is at an edge, then update positions of all aliens in the fleet"""
        self._check_fleet_edges()
        """Update the position of all aliens in the fleet"""
        self.aliens.update()

        """Look for alien-ship collisions"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        """Look for the aliens hitting bottom of the screen"""
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any alien reach the bottom of the screen"""
        screen_rect =  self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                """Treat it the same way as alien hit the ship"""
                self._ship_hit()
                break
    
    def _ship_hit(self):
        """Respond to the ship being hit by the alien"""
        if self.stats.ships_left > 0:

            """Decrement  ship)left to -1"""
            self.stats.ships_left -= 1

            self.sb.prep_ships()

            """Get rid of any aliens or bulets that are left"""
            self.aliens.empty()
            self.bullets.empty()

            """Create a new fleet and centered the ship"""
            self._create_fleet()
            self.ship.center_ship()

            """Pause game when hit"""
            sleep(1.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of Alien"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Dertermine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height +  2 *  alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond apropirately if any alien reaches the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        """Drop the entire fleet and change fleet directions"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
            
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        """Caling group's draw methid to draw alien ont the screen"""
        self.aliens.draw(self.screen)

        """Draw the score information"""
        self.sb.show_score()
        

        """Draw the play button if the game is Inactive"""
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

                   
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()