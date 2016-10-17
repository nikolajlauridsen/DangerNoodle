import pygame

class Settings:

    def __init__(self):
        # Colors
        self.colors = {
            "grey": (240, 248, 255),
            "red": (227, 38, 54),
            "green": (0, 128, 0),
            "metal": (96, 130, 182)
        }

        # Window options
        self.screen_size = [1280, 720]
        self.screen_middle = [self.screen_size[0]//2, self.screen_size[1]//2]

        # Player options
        self.snake_size = 25
        self.start_speed = 10

        self.score = 0

        # Running flags
        self.main_menu = True
        self.death_menu = False
        self.game_running = False
        self.settings_menu = False
        self.game_paused = False
