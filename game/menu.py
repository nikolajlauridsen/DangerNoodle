"""Various menu related classes such as string_writer and so on"""
import pygame
import game.events as event_handler
from game.buttons import Button


class StringWriter():
    """Class for drawing generic text to the screen"""
    def __init__(self, screen):
        self.screen = screen

    def draw_string(self, string, size, x, y):
        font = pygame.font.Font(None, size)       # Create font with desired size
        text = font.render(string, 1, (0, 0, 0))  # Create a text "sprite"
        text_rect = text.get_rect()               # get it's rect
        text_rect.centerx = x                     # and se it's location
        text_rect.centery = y
        self.screen.blit(text, text_rect)         # Lastly draw it to screen

class DeathScreen():
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock

    def run(self):
        while self.settings.death_menu:
            self.screen.fill(self.settings.colors["grey"])
            string_writer = StringWriter(self.screen)
            retry_yes = Button(self.settings.screen_size[0]//2,
                               self.settings.screen_size[1]//2, 250, 50,
                               self.settings.colors["green"],
                               "Yes", self.screen)
            retry_no = Button(self.settings.screen_size[0]//2 + 300,
                               self.settings.screen_size[1]//2, 250, 50,
                               self.settings.colors["green"],
                              "No", self.screen)
            string_writer.draw_string("Game over!", 75,
                                      self.settings.screen_size[0]//2,
                                      (self.settings.screen_size[1]//2)-200)
            string_writer.draw_string("Retry?", 50,
                                      self.settings.screen_size[0] // 2,
                                      (self.settings.screen_size[1] // 2) - 100)
            retry_yes.draw_button()
            retry_no.draw_button()
            event_handler.check_death_events(retry_yes, retry_no, self.settings)
            self.clock.tick(60)
            pygame.display.flip()


