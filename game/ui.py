"""UI classes like StringWriter and Buttons"""
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


class StringInputField:
    """Input field class for capturing input from the keyboard"""
    def __init__(self, screen, settings, x, y, limit=20,
                 default_text="Click to write...",
                 background_color=(255, 255, 255), width=500, height=50,
                 text_color=(0, 0, 0), border=6, border_color=(0, 0, 0)):
        self.screen = screen
        self.settings = settings
        self.x = x
        self.y = y
        self.limit = limit
        self.default_text = default_text
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

    def restore_defaults(self):
        self.keyboard_input = self.default_text
        self.capturing = False

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
                self.restore_defaults()

        elif event.type == pygame.QUIT:
            sys.exit()


class Button:
    """Button class for creating buttons"""
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


class IntSelector:
    def __init__(self, screen, settings, x, y, title, integer,
                 color=(96, 130, 182), min_int=0, max_int=999):
        self.screen = screen
        self.settings = settings
        self.title = title
        self.integer = integer
        self.x = x
        self.y = y
        self.min_int = min_int
        self.max_int = max_int

        # Labels
        self.title_label = StringWriter(self.screen, self.title, 20, x, y-50)
        self.display = StringWriter(self.screen, str(self.integer), 20,
                                    x, y)

        # Buttons
        # Plus
        self.plus_button = Button(x+100, y, 50, 50, color, "+", self.screen)
        self.plus_five_button = Button(x + 160, y, 50, 50, color, "+5",
                                       self.screen)
        # Minus
        self.minus_button = Button(x - 100, y, 50, 50, color, "-", self.screen)
        self.minus_five_button = Button(x - 160, y, 50, 50, color, "-5",
                                        self.screen)

    def get_int(self):
        return self.integer

    def draw(self):
        self.title_label.draw()
        self.display.draw()
        self.plus_button.draw_button()
        self.plus_five_button.draw_button()
        self.minus_button.draw_button()
        self.minus_five_button.draw_button()

    def check_events(self, event):
        if self.plus_button.pressed(event) and self.integer < self.max_int:
            self.integer += 1
            self.display.update_text(str(self.integer))
        elif self.plus_five_button.pressed(event) and self.integer+5 <= self.max_int:
            self.integer += 5
            self.display.update_text(str(self.integer))
        elif self.minus_button.pressed(event) and self.integer > self.min_int:
            self.integer -= 1
            self.display.update_text(str(self.integer))
        elif self.minus_five_button.pressed(event) and self.integer-5 >= self.min_int:
            self.integer -= 5
            self.display.update_text(str(self.integer))
