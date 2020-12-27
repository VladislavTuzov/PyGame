import sys

import pygame

from config import FPS
from classes.interface import MenuButton
from classes.exceptions import ExitPseudoError, NewGamePseudoError


def menu_screen(screen):
    pygame.mixer.music.load('source/music/menu.wav')

    clock = pygame.time.Clock()

    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.size

    background = pygame.image.load('source/fon_def.png')

    new_game_button = MenuButton('new_game')
    new_game_button.rect.x = (screen_width - new_game_button.rect.width) // 2
    new_game_button.rect.y = screen_height // 2 - new_game_button.rect.height * 1.25

    continue_button = MenuButton('continue')
    continue_button.rect.x = (screen_width - continue_button.rect.width) // 2
    continue_button.rect.y = screen_height // 2 + continue_button.rect.height // 4

    pygame.mixer.music.play(loops=-1, fade_ms=10000)

    screen.blit(background, (1, 1))
    screen.blit(new_game_button.image, new_game_button.rect)
    screen.blit(continue_button.image, continue_button.rect)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    continue
                elif new_game_button.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    raise NewGamePseudoError('start new game')
