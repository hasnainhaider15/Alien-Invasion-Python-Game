class GameStats:
    """Track Stats for Alien Invasion"""
    
    def __init__(self, ai_game):
        """Initialize Game statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        """Start alien invasion in an active state"""
        self.game_active = False

        """High score  should never be reset"""
        self.high_score = 0

        self.value = "HIGH SCORE"
        #self.level_text_value = "LEVEL"
    
    def reset_stats(self):
        """Initialize statsitcs than can chnage during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level =  0