"""UI objects like StringWriter and Buttons as well as menu classes"""
import pygame
import sys


class StringWriter():
    """Class for drawing generic text to the screen"""
    def __init__(self, screen, string, size, x, y):
        self.screen = screen
        self.font = pygame.font.Font(None, size)  # Create font with desired size
        self.text = self.font.render(string, 1, (0, 0, 0))  # Create a text "sprite"
        self.text_rect = self.text.get_rect()  # get it's rect
        self.text_rect.centerx = x  # and set it's location
        self.text_rect.centery = y

    def update_text(self, string):
        try:
            self.text = self.font.render(string, 1, (0, 0, 0))
        except TypeError:
            self.text = self.font.render(str(string), 1, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.text, self.text_rect)


class Button:
    def __init__(self, x, y, width, height, color, text, screen):
        self.screen = screen
        self.text = text

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.button_text = StringWriter(self.screen, text, 30,
                                        self.rect.centerx,
                                        self.rect.centery)

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.button_text.draw()

    def pressed(self, event):
        if event.pos[0] >= self.rect.left and event.pos[0] <= self.rect.right:
            if event.pos[1] >= self.rect.top and event.pos[1] <= self.rect.bottom:
                return True
        else:
            return False


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
        self.heading = StringWriter(screen, "Danger Noodle", 75,
                                    self.settings.screen_size[0] // 2,
                                    (self.settings.screen_size[1] // 2) - 200)

    def run(self):
        while self.settings.main_menu:
            self.screen.fill(self.settings.colors["grey"])
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.exit_button.draw_button()
            self.heading.draw()
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
        # Strings
        self.heading_string = StringWriter(self.screen, "Game over!", 75,
                                           self.settings.screen_size[0]//2,
                                           (self.settings.screen_size[1]//2)-200)

        self.score_string = StringWriter(self.screen,
                                         "Final Score: " + str(self.settings.score),
                                         50, self.settings.screen_size[0]//2,
                                         self.settings.screen_size[1]//2-125)

        self.retry_string = StringWriter(self.screen, "Retry?", 50,
                                         self.settings.screen_size[0] // 2,
                                         (self.settings.screen_size[1] // 2) - 50)

        # Buttons
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

            self.heading_string.draw()
            self.score_string.update_text("Final Score: " + str(self.settings.score))
            self.score_string.draw()
            self.retry_string.draw()
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

        # Strings
        self.snake_size_title = StringWriter(self.screen, "Snake Size:", 30,
                                             self.settings.screen_size[0]//2,
                                             self.settings.screen_size[1]//2-40)
        self.snake_size = StringWriter(self.screen,
                                       str(self.settings.snake_size), 25,
                                       self.settings.screen_size[0]//2,
                                       self.settings.screen_size[1]//2)

        # Buttons
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

    def run(self):
        while self.settings.settings_menu:
            self.screen.fill(self.settings.colors["grey"])
            self.snake_size_title.draw()
            self.snake_size.draw()
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
                    self.snake_size.update_text(str(self.settings.snake_size))
                elif self.snake_size_minus.pressed(event) and self.settings.snake_size > 2:
                    self.settings.snake_size -= 1
                    self.snake_size.update_text(str(self.settings.snake_size))
