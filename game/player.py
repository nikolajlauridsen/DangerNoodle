import pygame


class Player(pygame.sprite.Sprite):
    """Player class representing the snake"""

    def __init__(self, screen, settings):
        # Inherit from sprite class
        super().__init__()

        self.screen = screen
        self.settings = settings

        # Segment sizing
        self.segment_width = 20
        self.segment_height = 20
        # Space between each segment
        self.segment_margin = 3

        # Screen rect for screen edge detection
        self.screen_rect = screen.get_rect()

        # Movement vectors
        self.change_x = 0
        self.change_y = 0

        # Sprite group for player body segments
        self.player_sprites = pygame.sprite.Group()
        # Segment list for keeping track of sprite position
        # First item in the list is the "head" of the snake
        # the last item is the "tail" of the snake
        self.snake_segments = []

    def update(self):
        """Update method for the snake"""
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
            segment.rect.top = 0 + self.segment_margin + self.settings.overlay_width
        elif segment.rect.top < 0 + self.settings.overlay_width - self.segment_margin:
            segment.rect.bottom = self.settings.screen_size[1] - self.segment_margin

        # Collision detection
        body_hit_list = pygame.sprite.spritecollide(segment,
                                                    self.player_sprites, False)
        # If player hit itself stop game and start death menu
        if len(body_hit_list) > 0:
            self.settings.game_running = False
            self.settings.death_menu = True

        # Add player segment to segment list and player sprites
        self.snake_segments.insert(0, segment)
        self.player_sprites.add(segment)

    def create_snake(self):
        """Create the initial snake"""
        for i in range(self.settings.snake_size):
            # calculate x coordinates and set y
            # + = snake grows from left to right, - is the opposite
            x = 233 + (self.segment_width + self.segment_margin) * i
            y = 49 + self.settings.overlay_width
            # Create new segment
            segment = Segment(x, y, self.segment_width,
                              self.segment_height, self.settings)
            # Add to segment list and player sprites
            self.snake_segments.append(segment)
            self.player_sprites.add(segment)

    def add_segment(self):
        """Add a segment to the snake"""
        # Spawn segment out of the map to avoid collision
        x = -200
        y = -200
        segment = Segment(x, y, self.segment_width,
                          self.segment_height, self.settings)
        self.snake_segments.append(segment)
        self.player_sprites.add(segment)

    def show_direction(self, radius=10):
        """Show a circle displaying the direction of the player"""
        # Set rects new coordinates
        x = self.snake_segments[0].rect.centerx + self.change_x
        y = self.snake_segments[0].rect.centery + self.change_y
        # Draw a circle on the screen where the next segment will be
        pygame.draw.circle(self.screen, self.settings.colors["red"],
                           [x, y], radius, 0)

    def go_left(self):
        """Set player movement to left
        One direction is commented since it's practically the same
        for all directions."""
        # stop any up/down movement
        self.change_y = 0
        # Set new x movement vector
        # which is the width of a segment + the margin * -1
        # since x coordinates increase left to right so left is -
        self.change_x = (self.segment_width + self.segment_margin) * -1

    def go_right(self):
        """Set player movement to right"""
        self.change_y = 0
        self.change_x = (self.segment_width + self.segment_margin)

    def go_up(self):
        """Set player movement to up"""
        self.change_x = 0
        self.change_y = (self.segment_height + self.segment_margin) * -1

    def go_down(self):
        """Set player movement to down"""
        self.change_x = 0
        self.change_y = (self.segment_height + self.segment_margin)

    def draw(self, screen):
        """Draw the snake to the screen"""
        self.player_sprites.draw(screen)


class Segment(pygame.sprite.Sprite):
    """Segment class representing one segment of the snake"""
    def __init__(self, x, y, width, height, settings):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(settings.colors["red"])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
