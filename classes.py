import os
from math import hypot
from random import choice
from time import time

import pygame

from config import FPS
import helpers


class BaseHero(pygame.sprite.Sprite):
	def __init__(self, hero_name, hp, protection, weapon_limit=2):
		super().__init__()
		# pygame attributes
		self.image_left = pygame.image.load(f'source/heroes/{hero_name}/default_left.png')
		self.image_right = pygame.image.load(f'source/heroes/{hero_name}/default_right.png')

		self.image = self.image_left  # by default, then will be changed by direction
		self.rect = self.image.get_rect()

		self.speed = 180 / FPS  # pixels per second
		self.direction = [0, 0]

		# gameplay attributes
		self.hp = hp
		self.protection = protection

		self.weapons = Slots(weapon_limit)

	def change_direction(self, x_vector_change, y_vector_change):
		self.direction[0] += x_vector_change
		self.direction[1] += y_vector_change

		if self.direction[0] == -1:
			self.image = self.image_left
			self.weapon.image = self.weapon.image_left
		elif self.direction[0] == 1:
			self.image = self.image_right
			self.weapon.image = self.weapon.image_right

	def move(self, walls):
		x = self.rect.centerx + self.direction[0] * self.speed
		y = self.rect.centery + self.direction[1] * self.speed

		prev_center = self.rect.center
		self.rect.center = (x, y)

		if walls.colliderect(self.rect):
			self.rect.center = prev_center

		self.weapon.rect.center = (self.rect.centerx, self.rect.centery + 10)

	def shoot(self, pos):
		bullet = self.weapon.shoot(pos)
		return bullet

	@property
	def weapon(self):
		return self.weapons[0]

	def add_weapon(self, weapon):
		self.weapons.add_weapon(weapon)

	def change_weapon(self, weapon):
		self.weapons.change_weapon(weapon)

	def delete_weapon(self, weapon):
		if len(self.weapons) > 1:
			self.weapons.delete_weapon(weapon)

	def scroll(self):
		self.weapons.scroll()
		self.change_direction(0, 0)  # for change direction of weapon
	

class Slots(list):
	def __init__(self, limit):
		list.__init__(self)
		self.limit = limit

	def add_weapon(self, weapon):
		if len(self) < self.limit:
			self.append(weapon)

	def change_weapon(self, new_weapon):
		self[0] = new_weapon

	def delete_weapon(self):
		self[:] = self[1:]

	def scroll(self):
		self[:] = self[1:] + self[:1]


class Weapon(pygame.sprite.Sprite):
	def __init__(self, weapon_name, damage, cooldown):
		super().__init__()
		self.image_left = pygame.image.load(f'source/weapons/{weapon_name}/left.png')
		self.image_right = pygame.image.load(f'source/weapons/{weapon_name}/right.png')
		self.image = self.image_left  # by default, then will be change by direction
		self.rect = self.image.get_rect()

		self.weapon_name = weapon_name
		self.damage = damage
		self.cooldown = cooldown
		self.previous_shot_time = time() - self.cooldown - 0.00001

	def shoot(self, pos):
		shot_time = time()
		if shot_time - self.previous_shot_time >= self.cooldown:
			self.previous_shot_time = shot_time
			return Bullet(self.weapon_name, self.rect.center, pos, speed=420, damage=self.damage)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, weapon_name, start, pos, speed, damage):
		super().__init__()
		self.image = pygame.image.load(f'source/weapons/{weapon_name}/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = start

		self.speed = speed / FPS  # pixels by second
		self.damage = damage

		self.x0, self.y0 = start
		x1, y1 = pos
		self.current_distance = 0
		self.x_distance = x1 - self.x0
		self.y_distance = y1 - self.y0
		self.target_distance = hypot(self.x_distance, self.y_distance)

	def update(self, walls, enemies):
		self.current_distance += self.speed
		coeff = self.current_distance / self.target_distance

		x = self.x0 + self.x_distance * coeff
		y = self.y0 + self.y_distance * coeff
		prev_center = self.rect.center
		self.rect.center = (x, y)

		if walls.colliderect(self.rect):
			self.rect.center = prev_center
			self.kill()

		collided_enemies = enemies.colliderect(self.rect)
		if collided_enemies:
			enemy = collided_enemies[0]
			enemy.hit(self)
			self.kill()

		# self.current_distance -= self.speed
		# no reason for this line because we
		# deleted this bullet after wall collision


class Knight(BaseHero):
	def __init__(self):
		super().__init__('knight', hp=5, protection=5, weapon_limit=2)


class BaseEnemy(pygame.sprite.Sprite):
	def __init__(self, name, hp):
		super().__init__()
		self.image = pygame.image.load(f'source/enemies/{name}.png')
		self.rect = self.image.get_rect()

		self.hp = hp

	def hit(self, bullet):
		self.hp -= bullet.damage
		if self.hp <= 0:
			self.kill()


class Dardo(BaseEnemy):
	def __init__(self):
		super().__init__('dardo', hp=3)


class Room(pygame.sprite.Sprite):
	def __init__(self, pattern, floor_type: str):
		super().__init__()
		self.width = len(pattern[0])
		self.height = len(pattern)
		self.type = floor_type

		self.image = self._generate_image(pattern)
		self.rect = self.image.get_rect()

	def _generate_image(self, pattern):
		plate_size = get_image_size(self._get_random_plate())
		plate_width, plate_height = plate_size

		image_width = self.width * plate_width
		image_height = self.height * plate_height

		self.walls = helpers.RectList()

		image = pygame.Surface((image_width, image_height))
		for i, row in enumerate(pattern):
			for j, cell in enumerate(row):
				if cell == helpers.FLOOR:
					plate = pygame.image.load(self._get_random_plate())
					image.blit(plate, (plate_width * j, plate_height * i))
				elif cell == helpers.WALL:
					wall = pygame.image.load(self._get_random_wall())
					image.blit(wall, (plate_width * j, plate_height * i))
					self.walls.append(pygame.Rect((plate_width * j, plate_height * i,
												   plate_width, plate_height)))

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


def get_image_size(path):
	with open(path, 'rb') as file:
		data = file.read(24)
		width = int(data[16:20].hex(), 16)
		height = int(data[20:24].hex(), 16)
	return width, height


class MenuButton(pygame.sprite.Sprite):
	def __init__(self, button_name, x=0, y=0):
		super().__init__()
		self.image = pygame.image.load(f'source/buttons/{button_name}.png')
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

	def collidepoint(self, coords):
		return self.rect.collidepoint(coords)


class CustomCursor:
	def __init__(self, filename):
		self.image = pygame.image.load(f'source/cursors/{filename}')
		self.rect = self.image.get_rect()

	def update_pos(self, pos):
		self.rect.center = pos
