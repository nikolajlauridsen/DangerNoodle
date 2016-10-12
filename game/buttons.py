import pygame


class Button:
    def __init__(self, x, y, width, height, color, text, screen):

        self.screen = screen
        self.text = text

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.draw_string()

    def draw_string(self):
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, 1, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.centery = self.rect.centery
        self.screen.blit(text, text_rect)

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.draw_string()

    def pressed(self, event):
        if event.pos[0] >= self.rect.left and event.pos[0] <= self.rect.right:
            if event.pos[1] >= self.rect.top and event.pos[1] <= self.rect.bottom:
                print(event)
                print("x" + str(event.pos[0]) + " y " + str(event.pos[1]))
                return True
        else:
            return False
