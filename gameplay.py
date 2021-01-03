from functools import lru_cache
from io import BytesIO
from time import time

import pygame
from PIL import Image, ImageFilter

from config import (
    FPS, SCREEN_SIZE, SCREEN_CENTER,
    POINTS_TOPRIGHT_POS, BAR_TOPLEFT_POS
)
from classes.generation import Level
from classes.enemies import Dardo
from classes.exceptions import (
    PortalInteractPseudoError,
    ExitPseudoError, HeroDeath
)
from classes.interface import MenuButton
import helpers


def play(screen, font, cursor, hero, location="dungeon"):
    points = helpers.Points()
    level = Level(location)
    while True:
        try:
            # new level generates after midlevel screen
            level = play_level(screen, font, cursor, hero, level, location, points)
        except HeroDeath as e:
            gameover_screen(*e.args)
            return


def play_level(screen, font, cursor, hero, level, location, points):
    room = level.current_room
    hero.rect.center = room.hero_position
    while True:
        try:
            direction = play_room(screen, font, cursor, hero, room, points)
            level.update_position(*direction, hero)
            room = level.current_room

        except PortalInteractPseudoError as e:
            midlevel_screen(*e.args + (level.number,))
            new_level = Level(location)
            return new_level


def play_room(screen, font, cursor, hero, room, points):
    clock = pygame.time.Clock()

    enemies = helpers.EnemiesGroup()
    for enemy_spawnpoint in room.enemies_spawnpoints:
        enemy = Dardo()
        enemy.rect.center = enemy_spawnpoint
        enemies.add(enemy)

    bullets = pygame.sprite.Group()
    enemies_bullets = helpers.EnemiesBullets()

    mouse_pressed = False
    is_acceleration = False
    running = True
    while running:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                escape_menu(screen, hero, cursor)

            elif event.type == pygame.KEYDOWN:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(x_shift, y_shift)
                elif event.key == helpers.WEAPON_SCROLL:
                    hero.scroll()
                elif event.key == helpers.ACCELERATION:
                    is_acceleration = True
                elif event.key == helpers.INTERACTION:
                    try:
                        room.other_sprites.interact(hero)
                    except PortalInteractPseudoError:
                        # add args for mid-level screen
                        raise PortalInteractPseudoError(
                            screen, font, clock, hero, room, room.other_sprites)

            elif event.type == pygame.KEYUP:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(-x_shift, -y_shift)
                elif event.key == helpers.ACCELERATION:
                    is_acceleration = False

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

        screen.fill("black")

        screen.blit(room.image, room.rect)

        room.other_sprites.update()
        room.other_sprites.draw(screen)

        hero.move(room.walls, is_acceleration)
        hero.update_image()
        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        bullets.update(room.walls, enemies, points)
        bullets.draw(screen)

        try:
            enemies_bullets.update_as_enemies(room.walls, hero)
            enemies_bullets.draw(screen)
        except HeroDeath:
            # add args for gameover screen
            raise HeroDeath(screen, font, clock, hero, room, enemies)

        enemies.update(hero)
        enemies.shoot(hero.rect.center, enemies_bullets)
        enemies.draw(screen)
        enemies.draw_weapons(screen)

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
    surface = _render_text(
        font, f"HP: {hero.hp}  Stamina: {round(hero.stamina)}")
    screen.blit(surface, BAR_TOPLEFT_POS)


@lru_cache(maxsize=3)
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
    home_button = MenuButton("home", SCREEN_CENTER)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if home_button.collidepoint(pos):
                    raise ExitPseudoError("game exit")
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
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


def midlevel_screen(screen, font, clock, hero, room, sprites, level_number):
    background = screen.copy()
    background.fill("black")

    surface = _render_text(font, f"Level {level_number}")
    rect = surface.get_rect()
    rect.center = SCREEN_CENTER
    background.blit(surface, rect)

    start = time()
    while (elapsed_time := time() - start) < 2:
        screen.fill("black")

        screen.blit(room.image, room.rect)

        sprites.update()
        sprites.draw(screen)

        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        background.set_alpha(255 * elapsed_time / 1.9)
        screen.blit(background, (0, 0))

        pygame.display.flip()

        clock.tick(FPS)


def gameover_screen(screen, font, clock, hero, room, enemies):
    background = screen.copy()
    background.fill("black")

    surface = _render_text(font, "game over")
    rect = surface.get_rect()
    rect.center = SCREEN_CENTER
    background.blit(surface, rect)

    start = time()
    while (elapsed_time := time() - start) < 3:
        screen.fill("black")

        screen.blit(room.image, room.rect)

        enemies.draw(screen)
        enemies.draw_weapons(screen)

        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        background.set_alpha(255 * elapsed_time / 2)
        screen.blit(background, (0, 0))

        pygame.display.flip()

        clock.tick(FPS)
