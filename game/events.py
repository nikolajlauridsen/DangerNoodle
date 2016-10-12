import pygame
import sys


def check_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit("Game exited by user.")

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, player)
            break


def check_keydown_event(event, player):
    if event.key == pygame.K_ESCAPE:
        sys.exit("Game exited by user.")
    elif event.key == pygame.K_w and not player.change_y > 0:
        player.go_up()
    elif event.key == pygame.K_s and not player.change_y < 0:
        player.go_down()
    elif event.key == pygame.K_a and not player.change_x > 0:
        player.go_left()
    elif event.key == pygame.K_d and not player.change_x < 0:
        player.go_right()


def check_menu_events(start_button, exit_button, settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit('Game exited by user.')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.pressed(event):
                settings.game_running = True
            elif exit_button.pressed(event):
                sys.exit('Game exited by user.')

def check_death_events(retry_yes, retry_no, settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit('Game exited by user.')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if retry_yes.pressed(event):
                settings.game_running = True
                settings.death_menu = False
            elif retry_no.pressed(event):
                settings.game_running = False
                settings.death_menu = False


