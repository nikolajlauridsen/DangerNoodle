"""UI objects like StringWriter and Buttons as well as menu classes"""
import pygame
import sys


class StringWriter():
    """Class for drawing generic text to the screen"""
    def __init__(self, screen, string, size, x, y, color = (0, 0, 0)):
        self.screen = screen
        self.font = pygame.font.Font("freesansbold.ttf", size)  # Create font with desired size
        self.text = self.font.render(string, 1, color)  # Create a text "sprite"
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
    def __init__(self, x, y, width, height, color, text, screen, border=6,
                 border_color=(0, 0, 0)):
        self.screen = screen
        self.text = text

        self.image = pygame.Surface([width, height])
        self.border = pygame.Surface([width+border, height+border])
        self.image.fill(color)
        self.border.fill(border_color)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.border_rect = self.border.get_rect()
        self.border_rect.centerx = self.rect.centerx
        self.border_rect.centery = self.rect.centery
        self.button_text = StringWriter(self.screen, text, 30,
                                        self.rect.centerx,
                                        self.rect.centery)

    def draw_button(self):
        self.screen.blit(self.border, self.border_rect)
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
        self.play_button = Button(settings.screen_middle[0],
                                  settings.screen_middle[1], 200, 50,
                                  settings.colors["metal"], "Play", screen)
        self.settings_button = Button(settings.screen_middle[0],
                                      settings.screen_middle[1]+75, 200, 50,
                                      settings.colors["metal"], "Settings", screen)
        self.exit_button = Button(settings.screen_middle[0],
                                  settings.screen_middle[1]+150, 200, 50,
                                  settings.colors["metal"], "Exit", screen)
        self.heading = StringWriter(screen, "Danger Noodle", 75,
                                    self.settings.screen_middle[0],
                                    (self.settings.screen_middle[1]) - 200,
                                    color=self.settings.colors["green"])

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
        self.heading_string = StringWriter(self.screen, "Game over!", 70,
                                           self.settings.screen_middle[0],
                                           self.settings.screen_middle[1]-250)

        self.score_string = StringWriter(self.screen,
                                         "Final Score: " + str(self.settings.score),
                                         45, self.settings.screen_middle[0],
                                         self.settings.screen_middle[1]-175)

        self.retry_string = StringWriter(self.screen, "Retry?", 40,
                                         self.settings.screen_middle[0],
                                         (self.settings.screen_middle[1]) - 0)

        # Buttons
        self.retry_yes = Button(self.settings.screen_middle[0] - 150,
                                self.settings.screen_middle[1] + 75, 250, 50,
                                self.settings.colors["green"],
                                "Yes", self.screen)
        self.retry_no = Button(self.settings.screen_middle[0] + 150,
                               self.settings.screen_middle[1] + 75, 250, 50,
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
                    self.settings.score = 0
                elif self.retry_no.pressed(event):
                    self.settings.main_menu = True
                    self.settings.game_running = False
                    self.settings.death_menu = False
                    self.settings.score = 0


class SettingsMenu:
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock

        # Strings
        # Snake Size
        self.snake_size_title = StringWriter(self.screen, "Start size:", 25,
                                             self.settings.screen_middle[0],
                                             self.settings.screen_middle[1]-40)
        self.snake_size = StringWriter(self.screen,
                                       str(self.settings.snake_size), 20,
                                       self.settings.screen_middle[0],
                                       self.settings.screen_middle[1])
        # starting speed
        self.start_speed_title = StringWriter(self.screen, "Start speed:", 25,
                                              self.settings.screen_middle[0],
                                              self.settings.screen_middle[1] - 140)
        self.start_speed = StringWriter(self.screen,
                                        str(self.settings.start_speed), 20,
                                        self.settings.screen_middle[0],
                                        self.settings.screen_middle[1]-90)

        # Buttons
        # -------Snake Size Buttons-------
        self.snake_size_plus = Button(self.settings.screen_middle[0]+100,
                                     self.settings.screen_middle[1], 50, 50,
                                     self.settings.colors["green"],
                                     "+", self.screen)
        self.snake_size_plus_five = Button(self.settings.screen_middle[0]+160,
                                     self.settings.screen_middle[1], 50, 50,
                                     self.settings.colors["green"],
                                     "+5", self.screen)
        self.snake_size_minus = Button(self.settings.screen_middle[0]-100,
                                      self.settings.screen_middle[1], 50, 50,
                                      self.settings.colors["green"],
                                      "-", self.screen)
        self.snake_size_minus_five = Button(self.settings.screen_middle[0] - 160,
                                       self.settings.screen_middle[1], 50,
                                       50,
                                       self.settings.colors["green"],
                                       "-5", self.screen)
        # Start Speed Buttons
        self.start_speed_plus = Button(self.settings.screen_middle[0] + 100,
                                       self.settings.screen_middle[1] - 90, 50,
                                       50,
                                       self.settings.colors["green"],
                                       "+", self.screen)
        self.start_speed_plus_five = Button(self.settings.screen_middle[0] + 160,
                                           self.settings.screen_middle[1] - 90, 50, 50,
                                           self.settings.colors["green"],
                                           "+5", self.screen)
        self.start_speed_minus = Button(self.settings.screen_middle[0] - 100,
                                       self.settings.screen_middle[1] - 90, 50,
                                       50,
                                       self.settings.colors["green"],
                                       "-", self.screen)
        self.start_speed_minus_five = Button(self.settings.screen_middle[0] - 160,
                                             self.settings.screen_middle[1] - 90, 50,
                                             50,
                                             self.settings.colors["green"],
                                             "-5", self.screen)
        self.exit_button = Button(self.settings.screen_middle[0],
                                 self.settings.screen_middle[1]+75, 250, 50,
                                 self.settings.colors["green"],
                                 "Exit", self.screen)

    def run(self):
        while self.settings.settings_menu:
            self.screen.fill(self.settings.colors["grey"])
            # Snake size elements
            self.snake_size_title.draw()
            self.snake_size.draw()
            self.snake_size_plus.draw_button()
            self.snake_size_plus_five.draw_button()
            self.snake_size_minus.draw_button()
            self.snake_size_minus_five.draw_button()
            # Start speed elements
            self.start_speed_title.draw()
            self.start_speed.draw()
            self.start_speed_plus.draw_button()
            self.start_speed_plus_five.draw_button()
            self.start_speed_minus.draw_button()
            self.start_speed_minus_five.draw_button()
            # Exit elements
            self.exit_button.draw_button()
            self.check_events()
            # Tick and flip
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

                # Snake size events
                elif self.snake_size_plus.pressed(event):
                    self.settings.snake_size += 1
                    self.snake_size.update_text(str(self.settings.snake_size))

                elif self.snake_size_plus_five.pressed(event):
                    self.settings.snake_size += 5
                    self.snake_size.update_text(str(self.settings.snake_size))

                elif self.snake_size_minus.pressed(event) and self.settings.snake_size > 2:
                    self.settings.snake_size -= 1
                    self.snake_size.update_text(str(self.settings.snake_size))

                elif self.snake_size_minus_five.pressed(event) and self.settings.snake_size > 2:
                    self.settings.snake_size -= 5
                    self.snake_size.update_text(str(self.settings.snake_size))

                # Start speed events
                elif self.start_speed_plus.pressed(event):
                    self.settings.start_speed += 1
                    self.start_speed.update_text(str(self.settings.start_speed))

                elif self.start_speed_plus_five.pressed(event):
                    self.settings.start_speed += 5
                    self.start_speed.update_text(str(self.settings.start_speed))

                elif self.start_speed_minus.pressed(event):
                    self.settings.start_speed -= 1
                    self.start_speed.update_text(str(self.settings.start_speed))

                elif self.start_speed_minus_five.pressed(event):
                    self.settings.start_speed -= 5
                    self.start_speed.update_text(str(self.settings.start_speed))
