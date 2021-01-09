import sys

import pygame

from config import FPS, SCREEN_CENTER_X, SCREEN_CENTER_Y
from classes.interface import MenuButton
from classes.exceptions import ExitPseudoError, NewGamePseudoError
import db


def menu_screen(screen, font):
    new_game_button, high_scores_button = draw_menu(screen)

    pygame.mixer.music.load("source/music/menu.wav")
    pygame.mixer.music.play(loops=-1, fade_ms=10000)

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    raise NewGamePseudoError("New game")
                elif high_scores_button.collidepoint(event.pos):
                    high_scores_screen(screen, font)
                    draw_menu(screen)


def draw_menu(screen):
    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.size

    background = pygame.image.load("source/menu.png")

    shift = MenuButton("new_game", (0, 0)).rect.height // 1.5

    new_game_button = MenuButton(
        "new_game", (SCREEN_CENTER_X, SCREEN_CENTER_Y - shift))
    high_scores_button = MenuButton(
        "high_scores", (SCREEN_CENTER_X, SCREEN_CENTER_Y + shift))

    screen.blit(background, (1, 1))
    screen.blit(new_game_button.image, new_game_button.rect)
    screen.blit(high_scores_button.image, high_scores_button.rect)

    pygame.display.flip()

    return new_game_button, high_scores_button


def high_scores_screen(screen, font):
    table = db.extract()
    if table is None:
        table = ["no points yet"]

    screen.fill("black")

    font_height = font.render("17000", True, "white")\
                      .get_rect()\
                      .height

    height = len(table)
    total_height = font_height * (height * 2 - 1)
    start_y = SCREEN_CENTER_Y - total_height // 2 + font_height // 2

    for i, value in enumerate(table):
        surface = font.render(value, True, "white")
        rect = surface.get_rect()
        rect.centerx = SCREEN_CENTER_X
        rect.centery = start_y + font_height * i * 2
        screen.blit(surface, rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
