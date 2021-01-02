from functools import lru_cache
from io import BytesIO

import pygame
from PIL import Image, ImageFilter

from config import (
    FPS, SCREEN_SIZE, SCREEN_CENTER,
    POINTS_TOPRIGHT_POS, BAR_TOPLEFT_POS
)
from classes.generation import Level
from classes.enemies import Dardo
from classes.exceptions import PortalInteractPseudoError
from classes.interface import MenuButton
import helpers


def play_level(screen, font, cursor, hero, location='dungeon'):
    level = Level(location)
    room = level.current_room
    hero.rect.center = room.hero_position
    points = helpers.Points()
    while True:
        try:
            direction = play_room(screen, font, cursor, hero, room, points)
            if direction is not None:
                level.update_position(*direction, hero)
                room = level.current_room
            else:
                return
        except PortalInteractPseudoError:
            return


def play_room(screen, font, cursor, hero, room, points):
    clock = pygame.time.Clock()

    enemies = helpers.RectGroup()
    for enemy_spawnpoint in room.enemies_spawnpoints:
        enemy = Dardo()
        enemy.rect.center = enemy_spawnpoint
        enemies.add(enemy)

    bullets = pygame.sprite.Group()

    mouse_pressed = False
    running = True
    while running:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = escape_menu(screen, hero, cursor)

            elif event.type == pygame.KEYDOWN:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(x_shift, y_shift)
                elif event.key == helpers.WEAPON_SCROLL:
                    hero.scroll()
                elif event.key == helpers.INTERACTION:
                    room.other_sprites.interact(hero)

            elif event.type == pygame.KEYUP:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(-x_shift, -y_shift)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                hero.shoot(event.pos, bullets)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False

        if mouse_pressed:
            pos = pygame.mouse.get_pos()
            hero.shoot(pos, bullets)

        if not enemies:
            room.delete_enemies_spawns()

        screen.fill('black')

        screen.blit(room.image, room.rect)

        room.other_sprites.update()
        room.other_sprites.draw(screen)

        hero.move(room.walls)
        hero.update()
        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        bullets.update(room.walls, enemies, points)
        bullets.draw(screen)

        enemies.update(hero)
        enemies.draw(screen)

        blit_points(screen, font, points)
        blit_bar(screen, font, hero)
        blit_cursor(screen, cursor)

        pygame.display.flip()
        clock.tick(FPS)

        is_outside, direction = room.is_hero_outside_room(hero)
        if is_outside:
            return direction


def blit_points(screen, font, points):
    surface = _render_text(font, str(points))
    rect = surface.get_rect()
    rect.topright = POINTS_TOPRIGHT_POS
    screen.blit(surface, rect)


def blit_bar(screen, font, hero):
    surface = _render_text(font, f"HP: {hero.hp}")
    screen.blit(surface, BAR_TOPLEFT_POS)


@lru_cache(maxsize=2)
def _render_text(font, text):
    surface = font.render(text, True, "white")
    return surface


def blit_cursor(screen, cursor):
    cursor.update_pos(pygame.mouse.get_pos())
    screen.blit(cursor.image, cursor.rect)


def handle_movement(event):
    if event.key == helpers.UP:
        x_shift, y_shift = 0, -1
    elif event.key == helpers.LEFT:
        x_shift, y_shift = -1, 0
    elif event.key == helpers.DOWN:
        x_shift, y_shift = 0, +1
    elif event.key == helpers.RIGHT:
        x_shift, y_shift = +1, 0
    return x_shift, y_shift


def escape_menu(screen, hero, cursor):
    blurred_screen = blur_screen(screen)
    home_button = MenuButton("home", *SCREEN_CENTER)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if home_button.collidepoint(pos):
                    return False
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(x_shift, y_shift)

            elif event.type == pygame.KEYUP:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(-x_shift, -y_shift)

        screen.blit(blurred_screen, (0, 0))
        screen.blit(home_button.image, home_button.rect)
        blit_cursor(screen, cursor)

        pygame.display.flip()


def blur_screen(screen):
    string = pygame.image.tostring(screen, "RGB")
    image = Image.frombytes("RGB", SCREEN_SIZE, string, "raw")\
                 .filter(ImageFilter.GaussianBlur(radius=4))
    image.seek(0)

    blurred_image = BytesIO()
    image.save(blurred_image, "PNG")
    blurred_image.seek(0)

    blurred_image = pygame.image.load(blurred_image)
    return blurred_image
