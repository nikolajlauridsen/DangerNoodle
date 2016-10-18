"""UI objects like StringWriter and Buttons as well as menu classes"""
import pygame

import sys


class StringWriter:
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

    def reposition(self, x, y):
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = x
        self.text_rect.centery = y

    def draw(self):
        self.screen.blit(self.text, self.text_rect)


class StringInput:
    def __init__(self, screen, settings, x, y, limit=20,
                 default_text="Click to write...",
                 background_color=(255, 255, 255), width=500, height=50,
                 text_color=(0, 0, 0), border=6, border_color=(0, 0, 0)):
        self.screen = screen
        self.settings = settings
        self.x = x
        self.y = y
        self.limit = limit
        self.keyboard_input = default_text
        self.text_length = len(self.keyboard_input)
        self.capturing = False

        # Grahpics stuff
        # Text
        self.text = StringWriter(self.screen, self.keyboard_input, 25,
                                 self.x, self.y, color=text_color)
        # Input box
        self.image = pygame.Surface([width, height])
        self.image.fill(background_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        # Border
        self.border = pygame.Surface([width+border, height+border])
        self.border.fill(border_color)
        self.border_rect = self.border.get_rect()
        self.border_rect.centerx = self.x
        self.border_rect.centery = self.y

    def capture(self, event):
        if self.capturing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.capturing:
                    self.capturing = False
                elif event.key == pygame.K_BACKSPACE and len(self.keyboard_input) > 0:
                    self.keyboard_input = self.keyboard_input[:-1]
                elif len(self.keyboard_input) <= self.limit:
                    self.keyboard_input += event.unicode

    def draw_frame(self):
        if self.text_length != len(self.keyboard_input):
            self.text.update_text(self.keyboard_input)
            self.text.reposition(self.x, self.y)
            self.text_length = len(self.keyboard_input)
        self.screen.blit(self.border, self.border_rect)
        self.screen.blit(self.image, self.rect)
        self.text.draw()

    def check_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= self.rect.left and event.pos[0] <= self.rect.right:
                if event.pos[1] >= self.rect.top and event.pos[1] <= self.rect.bottom:
                    self.keyboard_input = ""
                    self.capturing = True
            else:
                self.capturing = False

        elif event.type == pygame.QUIT:
            sys.exit()


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
        self.play_button = Button(self.settings.screen_middle[0],
                                  self.settings.screen_middle[1], 200, 50,
                                  self.settings.colors["metal"], "Play",
                                  self.screen)

        self.settings_button = Button(self.settings.screen_middle[0],
                                      self.settings.screen_middle[1]+75, 200, 50,
                                      self.settings.colors["metal"], "Settings", screen)

        self.high_score_button = Button(self.settings.screen_middle[0],
                                        self.settings.screen_middle[1]+150,
                                        200, 50, self.settings.colors["metal"],
                                        "High Score", screen)

        self.exit_button = Button(settings.screen_middle[0],
                                  self.settings.screen_middle[1] + 225, 200,
                                  50,
                                  self.settings.colors["metal"], "Exit",
                                  screen)

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
            self.high_score_button.draw_button()
            self.heading.draw()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.pressed(event):
                    self.settings.main_menu = False
                    self.settings.game_running = True
                elif self.settings_button.pressed(event):
                    self.settings.main_menu = False
                    self.settings.settings_menu = True
                elif self.high_score_button.pressed(event):
                    self.settings.high_score = True
                    self.settings.main_menu = False
                elif self.exit_button.pressed(event):
                    sys.exit()


class DeathScreen:
    def __init__(self, screen, settings, clock, db):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.db = db
        self.high_score_saved = False
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
                                         (self.settings.screen_middle[1]) + 100)

        # Buttons
        self.retry_yes = Button(self.settings.screen_middle[0] - 150,
                                self.settings.screen_middle[1] + 175, 250, 50,
                                self.settings.colors["green"],
                                "Yes", self.screen)
        self.retry_no = Button(self.settings.screen_middle[0] + 150,
                               self.settings.screen_middle[1] + 175, 250, 50,
                               self.settings.colors["red"],
                               "No", self.screen)
        self.save_high_score = Button(self.settings.screen_middle[0],
                                      self.settings.screen_middle[1],
                                      250, 50, self.settings.colors["metal"],
                                      "Save highscore", self.screen)
        self.input = StringInput(self.screen, self.settings,
                                 self.settings.screen_middle[0],
                                 self.settings.screen_middle[1]-100)

    def run(self):
        while self.settings.death_menu:
            self.screen.fill(self.settings.colors["grey"])

            self.heading_string.draw()
            self.score_string.update_text("Final Score: " + str(self.settings.score))
            self.score_string.draw()
            self.retry_string.draw()
            self.retry_yes.draw_button()
            self.retry_no.draw_button()
            self.input.draw_frame()
            self.save_high_score.draw_button()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if not self.high_score_saved:
                self.input.check_pressed(event)
                self.input.capture(event)
            if event.type == pygame.QUIT:
                sys.exit()
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
                elif self.save_high_score.pressed(event) and not self.high_score_saved:
                    name = self.input.keyboard_input
                    score = self.settings.score
                    self.db.insert_highscore(score, name)
                    self.db.save_changes()
                    self.high_score_saved = True
                    self.input.keyboard_input = "Highscore Saved"


class PauseScreen:
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        # Strings
        self.title = StringWriter(self.screen, "Game Paused", 70,
                                  self.settings.screen_middle[0],
                                  self.settings.screen_middle[1]-150)

        self.menu_button = Button(self.settings.screen_middle[0],
                                  self.settings.screen_middle[1]+175,
                                  200, 50, self.settings.colors["metal"],
                                  "Exit to menu", self.screen)
        self.resume_button = Button(self.settings.screen_middle[0],
                                    self.settings.screen_middle[1]+100,
                                    200, 50, self.settings.colors["metal"],
                                    "Resume", self.screen)

    def run(self, player, food_sprite, score):
        while self.settings.game_paused:
            self.screen.fill(self.settings.colors["grey"])
            player.draw(self.screen)
            food_sprite.draw(self.screen)
            score.draw()
            self.title.draw()
            self.menu_button.draw_button()
            self.resume_button.draw_button()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.settings.game_paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_button.pressed(event):
                    self.settings.game_running = False
                    self.settings.game_paused = False
                    self.settings.main_menu = True
                elif self.resume_button.pressed(event):
                    self.settings.game_paused = False


class HighScore:
    def __init__(self, screen, settings, clock, db):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.db = db
        self.high_scores = self.db.get_highscore()
        self.high_score_labesls = []
        self.create_labels()
        self.backup_label = StringWriter(self.screen, "No high scores",
                                         50, self.settings.screen_middle[0],
                                         self.settings.screen_middle[1])
        self.title = StringWriter(self.screen, "High Scores",
                                  50, self.settings.screen_middle[0],
                                  self.settings.screen_middle[1]-275)
        self.main_menu_button = Button(self.settings.screen_middle[0],
                                       self.settings.screen_middle[1]+300,
                                       200, 50, self.settings.colors["metal"],
                                       "Main Menu", self.screen)

    def create_labels(self):
        for i, high_Score in enumerate(self.high_scores):
            text = str(high_Score["name"]) + ":      " + str(high_Score["score"])
            label = StringWriter(self.screen, text, 25,
                                self.settings.screen_middle[0],
                                self.settings.screen_middle[1] + (30*i))
            self.high_score_labesls.append(label)

    def run(self):
        while self.settings.high_score:
            self.screen.fill(self.settings.colors["grey"])
            self.title.draw()
            self.main_menu_button.draw_button()
            if len(self.high_score_labesls) > 0:
                for label in self.high_score_labesls:
                    label.draw()
            else:
                self.backup_label.draw()
            self.check_events()
            self.clock.tick(60)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu_button.pressed(event):
                    self.settings.high_score = False
                    self.settings.main_menu = True


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
                                     self.settings.colors["metal"],
                                     "+", self.screen)
        self.snake_size_plus_five = Button(self.settings.screen_middle[0]+160,
                                     self.settings.screen_middle[1], 50, 50,
                                     self.settings.colors["metal"],
                                     "+5", self.screen)
        self.snake_size_minus = Button(self.settings.screen_middle[0]-100,
                                      self.settings.screen_middle[1], 50, 50,
                                      self.settings.colors["metal"],
                                      "-", self.screen)
        self.snake_size_minus_five = Button(self.settings.screen_middle[0] - 160,
                                       self.settings.screen_middle[1], 50,
                                       50,
                                       self.settings.colors["metal"],
                                       "-5", self.screen)
        # Start Speed Buttons
        self.start_speed_plus = Button(self.settings.screen_middle[0] + 100,
                                       self.settings.screen_middle[1] - 90, 50,
                                       50,
                                       self.settings.colors["metal"],
                                       "+", self.screen)
        self.start_speed_plus_five = Button(self.settings.screen_middle[0] + 160,
                                           self.settings.screen_middle[1] - 90, 50, 50,
                                           self.settings.colors["metal"],
                                           "+5", self.screen)
        self.start_speed_minus = Button(self.settings.screen_middle[0] - 100,
                                       self.settings.screen_middle[1] - 90, 50,
                                       50,
                                       self.settings.colors["metal"],
                                       "-", self.screen)
        self.start_speed_minus_five = Button(self.settings.screen_middle[0] - 160,
                                             self.settings.screen_middle[1] - 90, 50,
                                             50,
                                             self.settings.colors["metal"],
                                             "-5", self.screen)
        self.exit_button = Button(self.settings.screen_middle[0],
                                 self.settings.screen_middle[1]+75, 250, 50,
                                 self.settings.colors["metal"],
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
                sys.exit()
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
