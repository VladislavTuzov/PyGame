import os
from random import choice

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT
import helpers
import patterns


class Level:
    def __init__(self, location):
        self.location = location
        self.scheme = patterns.get_random_scheme()
        self.current_position = [0, 0]  # will be changed by spawn and player
        self._parse_scheme()

    def _parse_scheme(self):
        self.matrix = [[None for _ in range(len(self.scheme[0]))]
                       for _ in range(len(self.scheme))]
        for i, row in enumerate(self.scheme):
            for j, cell in enumerate(row):
                if cell in helpers.ROOMS:
                    pattern = patterns.get_random_pattern(cell)
                    self._add_gates(pattern, i, j)
                    room = Room(self, pattern.pattern, self.location)
                    self.matrix[i][j] = room
                    if cell == helpers.SPAWN:
                        self.current_room = self.matrix[i][j]
                        self.current_position = [i, j]
                elif cell in helpers.TUNNELS:
                    tunnel = Tunnel(self, self.location, cell)
                    self.matrix[i][j] = tunnel
                else:
                    continue

    def _add_gates(self, pattern, i, j):
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                try:
                    near_cell = self.scheme[x][y]
                    if near_cell == helpers.V_TUNN:
                        if x == i - 1:
                            pattern.add_top_gate()
                        elif x == i + 1:
                            pattern.add_bottom_gate()
                    elif near_cell == helpers.H_TUNN:
                        if y == j - 1:
                            pattern.add_left_gate()
                        elif y == j + 1:
                            pattern.add_right_gate()
                except IndexError:
                    continue

    def update_position(self, x_shift, y_shift, hero):
        self.current_position[0] += x_shift
        self.current_position[1] += y_shift
        i, j = self.current_position
        self.current_room = self.matrix[j][i]
        if x_shift == +1:
            self.current_room.place_hero(hero, 'left')
        elif x_shift == -1:
            self.current_room.place_hero(hero, 'right')
        elif y_shift == +1:
            self.current_room.place_hero(hero, 'top')
        elif y_shift == -1:
            self.current_room.place_hero(hero, 'bottom')


class Location:
    def is_hero_outside_room(self, hero):
        if hero.rect.x < self.rect.x:
            self.parent_level.update_position(-1, 0, hero)
            return True
        elif hero.rect.topright[0] > self.rect.topright[0]:
            self.parent_level.update_position(+1, 0, hero)
            return True
        elif hero.rect.y < self.rect.y:
            self.parent_level.update_position(0, -1, hero)
            return True
        elif hero.rect.bottomright[1] > self.rect.bottomright[1]:
            self.parent_level.update_position(0, +1, hero)
            return True
        return False

    def place_hero(self, hero, direction):
        if direction == 'left':
            hero.rect.midleft = self.rect.midleft
            hero.rect.x += 10
        elif direction == 'right':
            hero.rect.midright = self.rect.midright
            hero.rect.x -= 10
        elif direction == 'top':
            hero.rect.midtop = self.rect.midtop
            hero.rect.y += 10
        elif direction == 'bottom':
            hero.rect.midbottom = self.rect.midbottom
            hero.rect.y += 10


class Room(Location):
    def __init__(self, level, pattern, location):
        self.parent_level = level
        self.width = len(pattern[0])
        self.height = len(pattern)
        self.location = location

        self.image = self._parse_pattern(pattern)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def _parse_pattern(self, pattern):
        plate_size = get_image_size(get_random_plate(self.location))
        plate_width, plate_height = plate_size

        image_width = self.width * plate_width
        image_height = self.height * plate_height

        image_half_width = image_width // 2
        image_half_height = image_height // 2

        screen_center_x = SCREEN_WIDTH // 2
        screen_center_y = SCREEN_HEIGHT // 2

        self.walls = helpers.RectList()
        self.gates = helpers.RectList()

        self.hero_position = (0, 0)
        self.enemies_spawnpoints = []

        image = pygame.Surface((image_width, image_height))
        for i, row in enumerate(pattern):
            for j, cell in enumerate(row):
                on_room_x = plate_width * j
                on_room_y = plate_height * i
                on_screen_x = screen_center_x - (image_half_width - on_room_x)
                on_screen_y = screen_center_y - (image_half_height - on_room_y)

                if cell == helpers.FLOOR:
                    plate = pygame.image.load(get_random_plate(self.location))
                    image.blit(plate, (on_room_x, on_room_y))

                elif cell == helpers.WALL:
                    wall = pygame.image.load(get_random_wall(self.location))
                    image.blit(wall, (on_room_x, on_room_y))
                    wall_rect = pygame.Rect((on_screen_x, on_screen_y,
                                             plate_width, plate_height))
                    self.walls.append(wall_rect)

                elif cell == helpers.GATES:
                    gate = pygame.image.load(get_random_gate(self.location))
                    image.blit(gate, (on_room_x, on_room_y))
                    gate_rect = pygame.Rect((on_screen_x, on_screen_y,
                                             plate_width, plate_height))
                    self.gates.append(gate_rect)

                elif cell == helpers.BIRTH:
                    self.hero_position = (on_screen_x, on_screen_y)
                    plate = pygame.image.load(get_random_plate(self.location))
                    image.blit(plate, (on_room_x, on_room_y))

                elif cell == helpers.ENEMY:
                    self.enemies_spawnpoints.append((on_screen_x, on_screen_y))
                    plate = pygame.image.load(get_random_plate(self.location))
                    image.blit(plate, (on_room_x, on_room_y))

                elif cell == helpers.PORTAL:
                    plate = pygame.image.load(get_random_plate(self.location))
                    image.blit(plate, (on_room_x, on_room_y))

        return image

    def close_gates(self):
        self.walls.extend(self.gates)

    def open_gates(self):
        self.walls[:] = [wall for wall in self.walls if wall not in self.gates]


class Tunnel(Location):
    def __init__(self, level, location, direction):
        self.parent_level = level
        self.location = location
        if direction == helpers.H_TUNN:
            self.image = self._create_horizontal()
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def _create_horizontal(self):
        plate_size = get_image_size(get_random_plate(self.location))
        plate_width, plate_height = plate_size

        image_width = SCREEN_WIDTH
        image_height = 5 * plate_height

        image = pygame.Surface((image_width, image_height))
        image_center = (image_width // 2, image_height // 2)
        image_center_x, image_center_y = image_center

        self.walls = helpers.RectList()

        for i in range(SCREEN_WIDTH // plate_width + 1):
            for j in range(5):
                on_room_x = plate_width * i
                on_room_y = plate_height * j
                on_screen_x = SCREEN_WIDTH // 2 - (image_center_x - on_room_x)
                on_screen_y = SCREEN_HEIGHT // 2 - (image_center_y - on_room_y)

                tile = pygame.image.load(get_random_plate(self.location))
                image.blit(tile, (on_room_x, on_room_y))

                if j == 0 or j == 4:
                    wall_rect = pygame.Rect((on_screen_x, on_screen_y,
                                             plate_width, plate_height))
                    self.walls.append(wall_rect)

        return image


def get_random_plate(location):
    return choice(get_plates(location))


def get_plates(location):
    path = f'source/locations/{location}/floor'
    plates = [f'{path}/{plate_filename}'
              for plate_filename in os.listdir(path)]
    return plates


def get_random_wall(location):
    return choice(get_walls(location))


def get_walls(location):
    path = f'source/locations/{location}/walls'
    walls = [f'{path}/{wall_filename}'
             for wall_filename in os.listdir(path)]
    return walls


def get_random_gate(location):
    return choice(get_gates(location))


def get_gates(location):
    path = f'source/locations/{location}/gates'
    gates = [f'{path}/{gate_filename}'
             for gate_filename in os.listdir(path)]
    return gates


def get_image_size(path):
    with open(path, 'rb') as file:
        data = file.read(24)
        width = int(data[16:20].hex(), 16)
        height = int(data[20:24].hex(), 16)
    return width, height
