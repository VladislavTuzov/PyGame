import os
from random import choice

import pygame

import helpers


class Room(pygame.sprite.Sprite):
    def __init__(self, pattern, floor_type: str):
        super().__init__()
        self.width = len(pattern[0])
        self.height = len(pattern)
        self.type = floor_type

        self.image = self._parse_pattern(pattern)
        self.rect = self.image.get_rect()

    def _parse_pattern(self, pattern):
        plate_size = get_image_size(self._get_random_plate())
        plate_width, plate_height = plate_size

        image_width = self.width * plate_width
        image_height = self.height * plate_height

        self.walls = helpers.RectList()
        self.gates = helpers.RectList()

        self.hero_position = (0, 0)
        self.enemies_spawnpoints = []

        image = pygame.Surface((image_width, image_height))
        for i, row in enumerate(pattern):
            for j, cell in enumerate(row):
                x = plate_width * j
                y = plate_height * i

                if cell == helpers.FLOOR:
                    plate = pygame.image.load(self._get_random_plate())
                    image.blit(plate, (x, y))

                elif cell == helpers.WALL:
                    wall = pygame.image.load(self._get_random_wall())
                    image.blit(wall, (x, y))
                    self.walls.append(pygame.Rect((x, y, plate_width, plate_height)))

                elif cell == helpers.GATES:
                    gate = pygame.image.load(self._get_random_gate())
                    image.blit(gate, (x, y))
                    self.gates.append(pygame.Rect((x, y, plate_width, plate_height)))

                elif cell == helpers.BIRTH:
                    self.hero_position = (x, y)
                    plate = pygame.image.load(self._get_random_plate())
                    image.blit(plate, (x, y))

                elif cell == helpers.ENEMY:
                    self.enemies_spawnpoints.append((x, y))
                    plate = pygame.image.load(self._get_random_plate())
                    image.blit(plate, (x, y))

        return image

    def _get_random_plate(self):
        return choice(self._get_plates())

    def _get_plates(self):
        path = f'source/locations/{self.type}/floor'
        plates = [f'{path}/{plate_filename}'
                  for plate_filename in os.listdir(path)]
        return plates

    def _get_random_wall(self):
        return choice(self._get_walls())

    def _get_walls(self):
        path = f'source/locations/{self.type}/walls'
        walls = [f'{path}/{wall_filename}'
                  for wall_filename in os.listdir(path)]
        return walls

    def _get_random_gate(self):
        return choice(self._get_gates())

    def _get_gates(self):
        path = f'source/locations/{self.type}/gates'
        gates = [f'{path}/{gate_filename}'
                  for gate_filename in os.listdir(path)]
        return gates

    def close_gates(self):
        self.walls.extend(self.gates)

    def open_gates(self):
        self.walls[:] = [wall for wall in self.walls if wall not in self.gates]


def get_image_size(path):
    with open(path, 'rb') as file:
        data = file.read(24)
        width = int(data[16:20].hex(), 16)
        height = int(data[20:24].hex(), 16)
    return width, height
