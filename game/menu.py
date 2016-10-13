"""Various menu related classes such as string_writer and so on"""
import pygame
import sys
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


class MainMenu:
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        play_button_x = settings.screen_size[0]//2
        play_button_y = settings.screen_size[1]//2
        self.play_button = Button(play_button_x, play_button_y, 200, 50,
                                  settings.colors["green"], "Play", screen)
        self.settings_button = Button(play_button_x, play_button_y+75, 200, 50,
                                      settings.colors["green"], "Settings", screen)
        self.exit_button = Button(play_button_x, play_button_y+150, 200, 50,
                                  settings.colors["green"], "Exit", screen)
        self.string_writer = StringWriter(screen)

    def run(self):
        while self.settings.main_menu:
            self.screen.fill(self.settings.colors["grey"])
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.exit_button.draw_button()
            self.string_writer.draw_string("Danger Noodle", 75,
                                           self.settings.screen_size[0] // 2,
                                           (self.settings.screen_size[1] // 2) - 200)
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('Game exited by user.')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.pressed(event):
                    self.settings.main_menu = False
                    self.settings.game_running = True
                elif self.settings_button.pressed(event):
                    self.settings.main_menu = False
                    self.settings.settings_menu = True
                elif self.exit_button.pressed(event):
                    sys.exit('Game exited by user.')


class DeathScreen:
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.string_writer = StringWriter(self.screen)
        self.retry_yes = Button(self.settings.screen_size[0] // 2 - 150,
                                self.settings.screen_size[1] // 2 + 25, 250, 50,
                                self.settings.colors["green"],
                                "Yes", self.screen)
        self.retry_no = Button(self.settings.screen_size[0] // 2 + 150,
                               self.settings.screen_size[1] // 2 + 25, 250, 50,
                               self.settings.colors["green"],
                               "No", self.screen)

    def run(self):
        while self.settings.death_menu:
            self.screen.fill(self.settings.colors["grey"])

            self.string_writer.draw_string("Game over!", 75,
                                           self.settings.screen_size[0]//2,
                                           (self.settings.screen_size[1]//2)-200)
            self.string_writer.draw_string("Final Score: " + str(self.settings.score),
                                           50,
                                           self.settings.screen_size[0]//2,
                                           self.settings.screen_size[1]//2-125)
            self.string_writer.draw_string("Retry?", 50,
                                           self.settings.screen_size[0] // 2,
                                           (self.settings.screen_size[1] // 2) - 50)
            self.retry_yes.draw_button()
            self.retry_no.draw_button()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('Game exited by user.')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.retry_yes.pressed(event):
                    self.settings.game_running = True
                    self.settings.death_menu = False
                elif self.retry_no.pressed(event):
                    self.settings.main_menu = True
                    self.settings.game_running = False
                    self.settings.death_menu = False


class SettingsMenu:
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
                    self.settings.main_menu = True
                elif self.snake_size_plus.pressed(event):
                    self.settings.snake_size += 1
                elif self.snake_size_minus.pressed(event) and self.settings.snake_size > 2:
                    self.settings.snake_size -= 1
