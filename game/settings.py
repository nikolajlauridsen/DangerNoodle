import pygame

class Settings:

    def __init__(self):
        # Colors
        self.colors = {
            "grey": (240, 248, 255),
            "red": (227, 38, 54),
            "green": (0, 128, 0)
        }

        # Window options
        self.screen_size = [1280, 720]

        self.score = 0

        # Running flags
        self.death_menu = False
        self.game_running = False

    def render_score(self, screen):
        score_font = pygame.font.Font(None, 35)
        score = score_font.render("Score: " + str(self.score), 1, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.centerx = self.screen_size[0] - 100
        score_rect.centery = 20
        screen.blit(score, score_rect)
