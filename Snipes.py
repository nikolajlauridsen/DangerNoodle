import pygame

from game.settings import Settings
from game.player import Player
from game.food import Food
import game.events as event


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
    food = Food(screen, settings)

    # Game loop
    while running:
        # Handle events
        event.check_events(player)
        # Fill the screen and redraw objects
        screen.fill(settings.colors["grey"])
        player.update()
        player.draw(screen)
        food.blitme()
        # Wait for clock
        clock.tick(10)
        # Refresh the screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
