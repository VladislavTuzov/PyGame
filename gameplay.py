import pygame

from config import FPS
from classes.generation import Room
from classes.enemies import Dardo
import helpers
from patterns import get_random_pattern


def play_level(screen, cursor, hero, location='dungeon'):
    clock = pygame.time.Clock()

    bullets = pygame.sprite.Group()

    room = Room(get_random_pattern(), location)
    hero.rect.center = room.hero_position

    enemies = helpers.RectGroup()
    for enemy_spawnpoint in room.enemies_spawnpoints:
        enemy = Dardo()
        enemy.rect.center = enemy_spawnpoint
        enemies.add(enemy)

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

            elif event.type == pygame.KEYUP:
                if event.key in helpers.MOVEMENT_KEYS:
                    x_shift, y_shift = handle_movement(event)
                    hero.change_direction(-x_shift, -y_shift)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                pos = event.pos
                bullet = hero.shoot(pos)
                if bullet:
                    bullets.add(bullet)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False

        hero.move(room.walls)
        if mouse_pressed:
            pos = pygame.mouse.get_pos()
            bullet = hero.shoot(pos)
            if bullet:
                bullets.add(bullet)

        screen.fill('black')

        screen.blit(room.image, room.rect)
        screen.blit(hero.image, hero.rect)
        screen.blit(hero.weapon.image, hero.weapon.rect)

        enemies.update()
        enemies.draw(screen)

        bullets.update(room.walls, enemies)
        bullets.draw(screen)

        cursor.update_pos(pygame.mouse.get_pos())
        screen.blit(cursor.image, cursor.rect)

        pygame.display.flip()
        clock.tick(FPS)


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
