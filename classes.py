import os
from random import choice

import pygame

from config import FPS


class Hero(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('source/heroes/knight.png')
		self.rect = self.image.get_rect()

		self.x = self.rect.centerx
		self.y = self.rect.centery

		self.speed = 90 / FPS # pixels per second
		self.direction = [0, 0]

	def change_direction(self, x_shift, y_shift):
		self.direction[0] += x_shift
		self.direction[1] += y_shift

	def move(self,):
		self.x += self.direction[0] * self.speed
		self.y += self.direction[1] * self.speed

		self.rect.center = (self.x, self.y)


class Floor(pygame.sprite.Sprite):
	def __init__(self, width, height, floor_type: str):
		super().__init__()
		self.width = width
		self.height = height
		self.type = floor_type

		self.image = self._generate_image()
		self.rect = self.image.get_rect()

	def _generate_image(self):
		plate_size = get_image_size(self._get_random_plate())
		plate_width, plate_height = plate_size

		image_width = self.width * plate_width
		image_height = self.height * plate_height

		image = pygame.Surface((image_width, image_height))
		for i in range(self.width):
			for j in range(self.height):
				plate = pygame.image.load(self._get_random_plate())
				image.blit(plate, (plate_width * i, plate_height * j))

		return image

	def _get_random_plate(self):
		return choice(self._get_plates())

	def _get_plates(self):
		path = f'source/locations/{self.type}/floor'
		plates = [f'{path}/{plate_filename}'
				  for plate_filename in os.listdir(path)]
		return plates


def get_image_size(path):
	from PIL import Image
	image = Image.open(path)
	return image.size