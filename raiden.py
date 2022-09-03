# pylint: disable=no-member

import random
import sys

import pygame

from battleship import Battleship
from bullet import Bullet
from button import Button
from game_stats import GameStats
from health import Health
from scoreboard import Scoreboard
from scout import Scout
from settings import Settings
from ship import Ship


class Raiden:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # Music Added
        # pygame.mixer.music.load('./sounds/bgmusic.mp3')
        # pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Raiden")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats= GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.scouts = pygame.sprite.Group()
        self.battleships = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_scouts()
                self._update_battleships()
                
            self._update_screen()

    def _check_events(self):
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
            self.stats.game_active = True

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.scouts.empty()
            self.battleships.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Move the ship to the right.
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        # Move the ship to the left.
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        # Move the ship to the up.
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        # Move the ship to the down.
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        # Press ESC to exit game.
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        # Pres J to fire bullets
        elif event.key == pygame.K_j:
               self._fire_bullet()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.x > self.screen.get_rect().width:
                 self.bullets.remove(bullet)
        
        self._check_bullet_scout_collisions()
        self._check_bullet_battleship_collisions()

    def _check_bullet_scout_collisions(self):
        # Respond to bullet-scout collisions
        # Remove any bullets and scouts that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.scouts, True, True)
        
        if collisions:
            for scouts in collisions.values():
                self.stats.score += self.settings.scout_points * len(scouts)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.scouts:
            # Destroy existing bullets and create new fleet.
            #self.bullets.empty()
            self._create_fleet()

    def _check_bullet_battleship_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.battleships, True, True)
        
        if collisions:
            for battleships in collisions.values():
                self.stats.score += self.settings.battleship_points * len(battleships)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.battleships:
            #self.bullets.empty()
            self._create_fleet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)    
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
    
            # Get rid of any remaining aliens and bullets.
            self.scouts.empty()
            self.battleships.empty()
            #self.bullets.empty()  
        else: 
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        if len(self.scouts) < self.settings.scouts_allowed:
            new_scout = Scout(self)
            self.scouts.add(new_scout)

        if len(self.battleships) < self.settings.battleships_allowed:
            new_battleship = Battleship(self)
            self.battleships.add(new_battleship)      
    
    def _update_screen(self):
            # Update images on the screen, and flip to the new screen.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            # Update image of enemy ships
            self.scouts.draw(self.screen)
            self.battleships.draw(self.screen)

            # Draw the score information
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.stats.game_active:
                self.play_button.draw_button()           

            # Make the most recently drawn screen visible.
            pygame.display.flip()

    def _update_battleships(self):
        for battleship in self.battleships.copy():
            if battleship.rect.x < -50:
                 self.battleships.remove(battleship)
        #Update the psotions of all battleships in the fleet.
        self.battleships.update()

        # Look for battleship & ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.battleships):
            self._ship_hit()

    def _update_scouts(self):       
        # Get rid of ships that have disappered.
        for scout in self.scouts.copy():
            if scout.rect.x < -50:
                 self.scouts.remove(scout)
        #Update the positions of all scouts in the fleet.
        self.scouts.update()

        # Look for scout & ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.scouts):
            self._ship_hit()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Raiden()
    ai.run_game()
