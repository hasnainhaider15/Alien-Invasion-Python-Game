import pygame.font
from pygame.sprite import Group

from ship import Ship


class ScoreBoard():
    """"A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scoring attribute"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        """Font settings for scoring information"""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.txtfont = pygame.font.SysFont(None, 15, bold=True)

        """Prepare the initiale scoring image"""
        self.prep_score()

        """For High score"""
        self.prep_high_score()
        """To display text"""
        self.text_image()
        #self.level_text()

        """TO display level"""
        self.prep_level()

        self.prep_ships()

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        """Turn the level into a randered image"""

        level_str = str(self.stats.level)
        self.level_image = self.txtfont.render(level_str, True, self.text_color, self.settings.bg_color)

        """Position the level below the score"""
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.top -10

    def prep_high_score(self):
        """Turn the high score image into rendered image"""

        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        """Center the high score at the top of the screen"""
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    def prep_score(self):
        """Turn the score into a rendered image"""

        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        
        
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        """Display the score at the top right of the screen"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    
    def text_image(self):
        """To display text"""
        text_str = str(self.stats.value) 
        self.txt_image = self.txtfont.render(text_str, True, self.text_color, self.settings.bg_color)

        self.txt_rect = self.txt_image.get_rect()
        self.txt_rect.centerx = self.high_score_rect.centerx
        self.txt_rect.top = self.high_score_rect.top -10 

    def show_score(self):
        """Draw score, level and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.txt_image, self.txt_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Checl to see if there is new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    
