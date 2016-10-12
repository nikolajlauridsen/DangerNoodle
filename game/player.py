import pygame
import sys

class Player(pygame.sprite.Sprite):

    def __init__(self, screen, settings):
        super().__init__()

        self.screen = screen
        self.settings = settings

        self.segment_width = 20
        self.segment_height = 20
        self.segment_margin = 3
        self.snake_segments = []
        self.screen_rect = screen.get_rect()

        # Movement vectors
        self.change_x = 0
        self.change_y = 0

        self.player_sprites = pygame.sprite.Group()

        # Player stats
        self.speed = 5

    def update(self):
        # Remove the rearest most sprite
        old_segment = self.snake_segments.pop()
        self.player_sprites.remove(old_segment)

        # Calculate the position for the new sprite
        x = self.snake_segments[0].rect.x + self.change_x
        y = self.snake_segments[0].rect.y + self.change_y
        segment = Segment(x, y, self.segment_width,
                          self.segment_height, self.settings)
        # Register whether a segment hit the edge of the screen
        # If so set the position of the new segment to the other edge of the screen
        if segment.rect.right > self.settings.screen_size[0] + self.segment_margin:
            segment.rect.left = 0 + self.segment_margin
        elif segment.rect.left < 0 - self.segment_margin:
            segment.rect.right = self.settings.screen_size[0] - self.segment_margin
        elif segment.rect.bottom > self.settings.screen_size[1] + self.segment_margin:
            segment.rect.top = 0 + self.segment_margin
        elif segment.rect.top < 0 - self.segment_margin:
            segment.rect.bottom = self.settings.screen_size[1] - self.segment_margin

        # Collision detection
        body_hit_list = pygame.sprite.spritecollide(segment,
                                                    self.player_sprites, False)
        if len(body_hit_list) > 0:
            self.settings.game_running = False
            self.settings.death_menu = True

        self.snake_segments.insert(0, segment)
        self.player_sprites.add(segment)

    def create_snake(self):
        for i in range(25):
            x = 250 + (self.segment_width + self.segment_margin) * i
            y = 30
            segment = Segment(x, y, self.segment_width,
                              self.segment_height, self.settings)
            self.snake_segments.append(segment)
            self.player_sprites.add(segment)

    def add_segment(self):
        # Spawn segment out of the map to avoid collision
        x = -200
        y = -200
        segment = Segment(x, y, self.segment_width,
                          self.segment_height, self.settings)
        self.snake_segments.append(segment)
        self.player_sprites.add(segment)

    def go_left(self):
        self.change_y = 0
        self.change_x = (self.segment_width + self.segment_margin) * -1

    def go_right(self):
        self.change_y = 0
        self.change_x = (self.segment_width + self.segment_margin)

    def go_up(self):
        self.change_x = 0
        self.change_y = (self.segment_height + self.segment_margin) * -1

    def go_down(self):
        self.change_x = 0
        self.change_y = (self.segment_height + self.segment_margin)

    def draw(self, screen):
        self.player_sprites.draw(screen)


class Segment(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, settings):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(settings.colors["red"])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
