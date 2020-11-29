import os
from random import choice

import pygame


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


def main():
	width, height = 600, 400
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Floor')

	floor = Floor(4, 3, 'dungeon')

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.fill((0, 0, 0))
		screen.blit(floor.image, floor.rect)
		pygame.display.flip()


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()