import pygame

from game.settings import Settings
from game.player import Player
from game.food import Food
from game.menus import *
from game.ui import *
from game.highscore import DbHandler
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

    # Highscore DB
    db = DbHandler()

    # Menus
    main_menu = MainMenu(screen, settings, clock)
    death_menu = DeathScreen(screen, settings, clock, db)
    pause_screen = PauseScreen(screen, settings, clock)
    settings_menu = SettingsMenu(screen, settings, clock)
    high_score = HighScore(screen, settings, clock, db)

    # Game score for game loop
    score = StringWriter(screen, "Score: " + str(settings.score), 35,
                         settings.screen_size[0] - 100, 20)

    # App loop
    while app_running:
        # Run different menus depending on running flags in settings
        main_menu.run()
        settings_menu.run()
        death_menu.run()
        high_score.run()

        # If the game_running flag is true reset playing field and create
        # game options
        if settings.game_running:
            # Create or recreate sprites and reset score
            settings.score = 0
            score.update_text("Score: " + str(settings.score))
            player = Player(screen, settings)
            player.create_snake()
            player.go_down()
            food_sprite = pygame.sprite.GroupSingle(Food(screen, settings))
        # Game loop
        while settings.game_running:
            # If pasuse flag is true jump into pause_screen
            pause_screen.run(player, food_sprite, score)
            # Game loop
            # Handle events
            event_handler.check_events(player, settings)
            # Fill the screen and redraw objects
            screen.fill(settings.colors["grey"])
            food_sprite.sprite.collision_detect(player, food_sprite, score)
            player.update()
            player.draw(screen)
            food_sprite.draw(screen)
            score.draw()
            # Wait for clock
            clock.tick(settings.start_speed + (settings.score // 4))
            # Refresh the screen
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
