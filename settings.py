

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1300
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_width = 100
        self.ship_height = 25
        self.ship_color = (0, 255, 0)
        self.ship_speed = 1.5
        # Number of hits ship can take before ship dies.
        self.ship_limit = 5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 20
        self.bullet_height = 3
        self.bullet_color = (135, 206, 235)
        self.bullets_allowed = 5

        # Different ship movement speed
        self.scout_speed = 1
        self.battleship_speed = 0.5
        
        # Different ship scoring
        self.scout_points = 100
        self.battleship_points = 1000

        # Number of ship allowed
        self.scouts_allowed = 5
        self.battleships_allowed = 1

        
