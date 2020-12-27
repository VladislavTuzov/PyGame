import pygame

from config import FPS
from classes.generation import Level
from classes.enemies import Dardo
from classes.exceptions import PortalInteractPseudoError
import helpers


def play_level(screen, cursor, hero, location='dungeon'):
    level = Level(location)
    room = level.current_room
    hero.rect.center = room.hero_position
    while True:
        try:
            direction = play_room(screen, cursor, hero, room)
            if direction is not None:
                level.update_position(*direction, hero)
                room = level.current_room
            else:
                return
        except PortalInteractPseudoError:
            return


def play_room(screen, cursor, hero, room):
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
                running = False

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
                pos = event.pos
                bullet = hero.shoot(pos, bullets)

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
        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        bullets.update(room.walls, enemies)
        bullets.draw(screen)

        enemies.update(hero)
        enemies.draw(screen)

        blit_cursor(screen, cursor)

        pygame.display.flip()
        clock.tick(FPS)

        is_outside, direction = room.is_hero_outside_room(hero)
        if is_outside:
            return direction


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
