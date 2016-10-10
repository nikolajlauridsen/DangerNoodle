import pygame

from game.settings import Settings
from game.player import Player
from game.food import Food
import game.events as event_handler


def main():
    # --- Set the Stage ---
    pygame.init()

    # Create settings object
    settings = Settings()

    # Create Screen
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Snipes")

    # Create clock
    clock = pygame.time.Clock()

    # Running flag
    running = True

    # Create initial sprites
    player = Player(screen, settings)
    player.create_snake()
    player.go_down()
    food_sprite = pygame.sprite.GroupSingle(Food(screen, settings))
    
    # Game loop
    while running:
        # Handle events
        event_handler.check_events(player)
        # Fill the screen and redraw objects
        screen.fill(settings.colors["grey"])
        food_sprite.sprite.collision_detect(player, food_sprite)
        player.update()
        player.draw(screen)
        food_sprite.draw(screen)
        settings.render_score(screen)
        # Wait for clock
        clock.tick(10 + (settings.score//2))
        # Refresh the screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
