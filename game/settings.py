class Settings:

    def __init__(self):
        # Colors
        self.colors = {
            "grey": (240, 248, 255),
            "d-grey": (105,184,255),
            "red": (227, 38, 54),
            "green": (0, 128, 0),
            "metal": (96, 130, 182)
        }
#
        # Window options
        # Screen size is a bit weird because it must fall on this line
        # y = (player.segment_size + player.segment_margin) * x + play.segment_margin
        # Where x is the desired amount of segments "space" on the scree
        # and y is the required amount of pixels
        # IE: 23 * 31 + (3 + 150) = 716 (so the screen is 31 segments tall)
        self.overlay_width = 50
        self.screen_size = [1268, 716 + self.overlay_width]
        self.screen_middle = [self.screen_size[0]//2, self.screen_size[1]//2]

        # Player options
        self.snake_size = 25
        self.start_speed = 10

        # Game score
        self.score = 0
        self.max_speed = 80

        # Running flags
        self.main_menu = True
        self.death_menu = False
        self.game_running = False
        self.settings_menu = False
        self.game_paused = False
        self.high_score = False
