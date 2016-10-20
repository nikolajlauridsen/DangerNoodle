"""Menu classes"""
from game.ui import *
import pygame


class MainMenu:
    """Class for the main menu of the game"""
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

        self.how_to_button = Button(self.settings.screen_middle[0],
                                    self.settings.screen_middle[1] + 225,
                                    200, 50, self.settings.colors["metal"],
                                    "How to", screen)

        self.exit_button = Button(settings.screen_middle[0],
                                  self.settings.screen_middle[1] + 300, 200,
                                  50, self.settings.colors["metal"], "Exit",
                                  screen)

        self.heading = StringWriter(screen, "Danger Noodle", 75,
                                    self.settings.screen_middle[0],
                                    (self.settings.screen_middle[1]) - 200,
                                    color=self.settings.colors["green"])

    def run(self):
        while self.settings.main_menu:
            self.screen.fill(self.settings.colors["grey"])

            self.heading.draw()
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.high_score_button.draw_button()
            self.how_to_button.draw_button()
            self.exit_button.draw_button()

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
                elif self.how_to_button.pressed(event):
                    self.settings.how_to = True
                    self.settings.main_menu = False
                elif self.exit_button.pressed(event):
                    sys.exit()


class DeathScreen:
    """Menu class for the deathscreen displayed when you die"""
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
        self.input = StringInputField(self.screen, self.settings,
                                      self.settings.screen_middle[0],
                                      self.settings.screen_middle[1] - 75)

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
            if event.type == pygame.KEYDOWN:
                if not self.high_score_saved and event.key != pygame.K_RETURN:
                    self.input.capture(event)
                elif event.key == pygame.K_RETURN and self.input.capturing:
                    name = self.input.keyboard_input
                    score = self.settings.score
                    self.db.insert_highscore(score, name)
                    self.db.save_changes()
                    self.high_score_saved = True
                    self.input.keyboard_input = "Highscore Saved"

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input.check_pressed(event)
                if self.retry_yes.pressed(event):
                    self.settings.game_running = True
                    self.settings.death_menu = False
                    self.high_score_saved = False
                    self.input.restore_defaults()
                    self.settings.score = 0
                elif self.retry_no.pressed(event):
                    self.settings.main_menu = True
                    self.settings.game_running = False
                    self.settings.death_menu = False
                    self.high_score_saved = False
                    self.input.restore_defaults()
                    self.settings.score = 0
                elif self.save_high_score.pressed(event) and not self.high_score_saved:
                    name = self.input.keyboard_input
                    score = self.settings.score
                    self.db.insert_highscore(score, name)
                    self.db.save_changes()
                    self.high_score_saved = True
                    self.input.keyboard_input = "Highscore Saved"


class PauseScreen:
    """Menu class for the pause screen of the game"""
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

    def run(self, player, food_sprite, game_overlay):
        while self.settings.game_paused:
            self.screen.fill(self.settings.colors["grey"])
            player.draw(self.screen)
            player.show_direction()
            food_sprite.draw(self.screen)
            game_overlay.draw(player)
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
    """Menu class for the high score menu"""
    def __init__(self, screen, settings, clock, db):
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.db = db
        self.high_scores = []
        self.high_score_labels = []
        self.create_labels()
        self.backup_label = StringWriter(self.screen, "No high scores",
                                         50, self.settings.screen_middle[0],
                                         self.settings.screen_middle[1])
        self.title = StringWriter(self.screen, "High Scores",
                                  50, self.settings.screen_middle[0], 50)
        self.main_menu_button = Button(self.settings.screen_middle[0],
                                       self.settings.screen_middle[1]+300,
                                       200, 50, self.settings.colors["metal"],
                                       "Main Menu", self.screen)

    def create_labels(self):
        """Create text labels"""
        # Make title labels and add to list
        rank_title = StringWriter(self.screen, "Rank", 35,
                                  self.settings.screen_middle[0] - 250,
                                  self.settings.screen_middle[1] - 250)
        name_titel = StringWriter(self.screen, "Name", 35,
                                self.settings.screen_middle[0],
                                self.settings.screen_middle[1] - 250)
        score_title = StringWriter(self.screen, "Score", 35,
                                   self.settings.screen_middle[0] + 250,
                                   self.settings.screen_middle[1] - 250)
        self.high_score_labels.append(rank_title)
        self.high_score_labels.append(name_titel)
        self.high_score_labels.append(score_title)
        # for every entry in highscores make a label and add it to list
        for i, high_Score in enumerate(self.high_scores):
            name = high_Score["name"]
            score = str(high_Score["score"])
            rank_label = StringWriter(self.screen, str(i+1), 25,
                                      self.settings.screen_middle[0] - 250,
                                      self.settings.screen_middle[1] + (30*i) - 200)
            name_label = StringWriter(self.screen, name, 25,
                                self.settings.screen_middle[0],
                                self.settings.screen_middle[1] + (30*i) - 200)
            score_label = StringWriter(self.screen, score, 25,
                                       self.settings.screen_middle[0] + 250,
                                       self.settings.screen_middle[1] + (30*i) - 200)
            self.high_score_labels.append(rank_label)
            self.high_score_labels.append(name_label)
            self.high_score_labels.append(score_label)

    def populate_high_score(self):
        """Get high scores from db and make labels"""
        self.high_scores = self.db.get_highscore()
        self.create_labels()

    def run(self):
        while self.settings.high_score:
            if len(self.high_scores) < 1:
                self.populate_high_score()
            self.screen.fill(self.settings.colors["grey"])
            self.title.draw()
            self.main_menu_button.draw_button()
            if len(self.high_scores) > 0:
                for label in self.high_score_labels:
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
                    self.high_scores = []
                    self.high_score_labels = []
                    self.settings.high_score = False
                    self.settings.main_menu = True


class SettingsMenu:
    """Menu class for the settings menu of the game"""
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock

        # Strings
        # Snake Size
        self.title = StringWriter(self.screen, "Settings", 50,
                                  self.settings.screen_middle[0], 50)
        # Int input
        self.snake_size_input = IntSelector(self.screen,
                                            self.settings.screen_middle[0],
                                            self.settings.screen_middle[1] + 40,
                                            "Snake size:",
                                            self.settings.snake_size, min_int=2)

        self.max_speed_input = IntSelector(self.screen,
                                           self.settings.screen_middle[0],
                                           self.settings.screen_middle[1] - 60,
                                           "Max Speed:", self.settings.max_speed,
                                           max_int=200)

        self.start_speed_input = IntSelector(self.screen,
                                             self.settings.screen_middle[0],
                                             self.settings.screen_middle[1] - 160,
                                             "Start Speed:", self.settings.start_speed,
                                             min_int=5, max_int=60)
        # Buttons
        self.exit_button = Button(self.settings.screen_middle[0],
                                 self.settings.screen_middle[1]+300, 200, 50,
                                 self.settings.colors["metal"],
                                 "Main menu", self.screen)

    def run(self):
        while self.settings.settings_menu:
            self.screen.fill(self.settings.colors["grey"])
            self.title.draw()
            # Snake size elements
            self.snake_size_input.draw()
            # Start speed elements
            self.start_speed_input.draw()
            # Max speed elements
            self.max_speed_input.draw()
            # Exit elements
            self.exit_button.draw_button()
            self.check_events()
            # Tick and flip
            self.clock.tick(60)
            pygame.display.flip()

    def save_settings(self):
        self.settings.max_speed = self.max_speed_input.get_int()
        self.settings.snake_size = self.snake_size_input.get_int()
        self.settings.start_speed = self.start_speed_input.get_int()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.max_speed_input.check_events(event)
                self.snake_size_input.check_events(event)
                self.start_speed_input.check_events(event)

                if self.exit_button.pressed(event):
                    self.save_settings()
                    self.settings.settings_menu = False
                    self.settings.game_running = False
                    self.settings.main_menu = True


class HowToPlay:
    def __init__(self, screen, settings, clock):
        self.screen = screen
        self.settings = settings
        self.clock = clock

        # Text lables
        self.labels = []
        self.create_labels()
        self.title_label = StringWriter(self.screen, "How to play", 50,
                                        self.settings.screen_middle[0], 50)

        # Buttons
        self.exit_button = Button(self.settings.screen_middle[0],
                                  self.settings.screen_middle[1]+300,
                                  200, 50, self.settings.colors["metal"],
                                  "Main Menu", self.screen)

    def create_labels(self):
        texts = [
            ("Move up", "W or up arrow"),
            ("Move down", "S or down arrow"),
            ("Move left", "A or left arrow"),
            ("Move right", "D or right arrow"),
            ("Pause Game", "Esc")
        ]
        for i, text in enumerate(texts):
            button = StringWriter(self.screen, text[0], 25,
                                  self.settings.screen_middle[0]-200,
                                  i*75 + (self.settings.screen_middle[1]-150))
            description = StringWriter(self.screen, text[1], 25,
                                       self.settings.screen_middle[0]+200,
                                       i*75 + (self.settings.screen_middle[1]-150))
            self.labels.append(button)
            self.labels.append(description)

    def run(self):
        while self.settings.how_to:
            self.screen.fill(self.settings.colors["grey"])
            # Draw labels
            self.title_label.draw()
            for label in self.labels:
                label.draw()
            self.exit_button.draw_button()
            self.clock.tick(60)
            self.check_events()
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.pressed(event):
                    self.settings.how_to = False
                    self.settings.main_menu = True
