import pygame

from game.settings import Settings
from game.player import Player
from game.food import Food
from game.ui import *
import game.events as event_handler


def main():
    # --- Set the Stage ---
    pygame.init()

    # Create settings object
    settings = Settings()

    # Create Screen
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Danger Noodle")

    # Create clock
    clock = pygame.time.Clock()

    # Running flags
    app_running = True

    # Menus
    main_menu = MainMenu(screen, settings, clock)
    death_menu = DeathScreen(screen, settings, clock)
    settings_menu = SettingsMenu(screen, settings, clock)

    # Game score for game loop
    score = StringWriter(screen, "Score: " + str(settings.score), 35,
                         settings.screen_size[0] - 100, 20)

    while app_running:
        # App loop
        # Run different menus depending on running flags in settings
        main_menu.run()
        settings_menu.run()
        death_menu.run()

        if settings.game_running:
            # Create or recreate sprites and reset score
            settings.score = 0
            score.update_text("Score: " + str(settings.score))
            player = Player(screen, settings)
            player.create_snake()
            player.go_down()
            food_sprite = pygame.sprite.GroupSingle(Food(screen, settings))
        while settings.game_running:
            # Game loop
            # Handle events
            event_handler.check_events(player, settings)
            # Wait for clock
            clock.tick(settings.start_speed + (settings.score // 4))
            # Fill the screen and redraw objects
            if not settings.game_paused:
                screen.fill(settings.colors["grey"])
                food_sprite.sprite.collision_detect(player, food_sprite, score)
                player.update()
                player.draw(screen)
                food_sprite.draw(screen)
                score.draw()

                # Refresh the screen
                pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
