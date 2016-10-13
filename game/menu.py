"""Various menu related classes such as string_writer and so on"""
import pygame
import sys
import game.events as event_handler
from game.buttons import Button


class StringWriter():
    """Class for drawing generic text to the screen"""
    def __init__(self, screen):
        self.screen = screen

    # TODO: Make this more efficient (No reason to create a new font object
    # and text rect on every pass (this function alones takes up 6,4% of
    # cpu time
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
        if self.settings.death_menu:
            string_writer = StringWriter(self.screen)
            retry_yes = Button(self.settings.screen_size[0] // 2 - 150,
                               self.settings.screen_size[1] // 2 + 25, 250, 50,
                               self.settings.colors["green"],
                               "Yes", self.screen)
            retry_no = Button(self.settings.screen_size[0] // 2 + 150,
                              self.settings.screen_size[1] // 2 + 25, 250, 50,
                              self.settings.colors["green"],
                              "No", self.screen)
        while self.settings.death_menu:
            self.screen.fill(self.settings.colors["grey"])

            string_writer.draw_string("Game over!", 75,
                                      self.settings.screen_size[0]//2,
                                      (self.settings.screen_size[1]//2)-200)
            string_writer.draw_string("Final Score: " + str(self.settings.score),
                                      50,
                                      self.settings.screen_size[0]//2,
                                      self.settings.screen_size[1]//2-125)
            string_writer.draw_string("Retry?", 50,
                                      self.settings.screen_size[0] // 2,
                                      (self.settings.screen_size[1] // 2) - 50)
            retry_yes.draw_button()
            retry_no.draw_button()
            event_handler.check_death_events(retry_yes, retry_no, self.settings)
            self.clock.tick(60)
            pygame.display.flip()


class SettingsMenu():
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.snake_size_plus = Button(self.settings.screen_size[0]//2+100,
                                     self.settings.screen_size[1]//2, 50, 50,
                                     self.settings.colors["green"],
                                     "+", self.screen)
        self.snake_size_minus = Button(self.settings.screen_size[0] // 2-100,
                                      self.settings.screen_size[1] // 2, 50, 50,
                                      self.settings.colors["green"],
                                      "-", self.screen)
        self.exit_button = Button(self.settings.screen_size[0]//2,
                                 self.settings.screen_size[1]//2+75, 250, 50,
                                 self.settings.colors["green"],
                                 "Exit", self.screen)
        self.string_writer = StringWriter(self.screen)

    def run(self):
        while self.settings.settings_menu:
            self.screen.fill(self.settings.colors["grey"])
            self.string_writer.draw_string("Snake Size:", 30,
                                      self.settings.screen_size[0]//2,
                                      self.settings.screen_size[1]//2-40)
            self.string_writer.draw_string(str(self.settings.snake_size), 25,
                                           self.settings.screen_size[0]//2,
                                           self.settings.screen_size[1]//2)
            self.snake_size_plus.draw_button()
            self.snake_size_minus.draw_button()
            self.exit_button.draw_button()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Game exited by user")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.pressed(event):
                    self.settings.settings_menu = False
                    self.settings.game_running = False
                elif self.snake_size_plus.pressed(event):
                    self.settings.snake_size += 1
                elif self.snake_size_minus.pressed(event) and self.settings.snake_size > 1:
                    self.settings.snake_size -= 1
