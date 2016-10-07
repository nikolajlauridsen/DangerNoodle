import pygame
import random

class Food(pygame.sprite.Sprite):

    def __init__(self, screen, settings):
        super().__init__()

        self.screen = screen
        self.settings = settings

        # Load graphic
        self.image = pygame.Surface([10, 10])
        self.image.fill(self.settings.colors["green"])
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(0, self.settings.screen_size[0])
        self.rect.centery = random.randint(0, self.settings.screen_size[1])

    def collision_detect(self, player_sprites, food_sprite):
        hit_list = pygame.sprite.spritecollide(self, player_sprites, True)
        if len(hit_list) > 0:
            self.kill()
            print("You got a point!")
            food_sprite.add(Food(self.screen, self.settings))

    def blitme(self):
        """Draw the food"""
        self.screen.blit(self.image, self.rect)
