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

        self.rect.centerx = random.randint(10, self.settings.screen_size[0]-5)
        self.rect.centery = random.randint(10, self.settings.screen_size[1]-5)

    def collision_detect(self, player, food_sprite, score):
        hit_list = pygame.sprite.spritecollide(self, player.player_sprites, False)
        if len(hit_list) > 0:
            self.kill()
            self.settings.score += 1
            score.update_text("Score: " + str(self.settings.score))
            player.add_segment()
            food_sprite.add(Food(self.screen, self.settings))
