import sys

import pygame

from config import FPS, SCREEN_CENTER
from classes.interface import MenuButton
from classes.exceptions import ExitPseudoError, NewGamePseudoError


def menu_screen(screen):
    pygame.mixer.music.load('source/music/menu.wav')

    clock = pygame.time.Clock()

    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.size

    background = pygame.image.load('source/fon_def.png')
    new_game_button = MenuButton('new_game', SCREEN_CENTER)

    pygame.mixer.music.play(loops=-1, fade_ms=10000)

    screen.blit(background, (1, 1))
    screen.blit(new_game_button.image, new_game_button.rect)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    raise NewGamePseudoError('start new game')
