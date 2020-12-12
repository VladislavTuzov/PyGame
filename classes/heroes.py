from collections import deque

import pygame

from config import FPS


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

		self.weapons = WeaponSlots(weapon_limit)

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


class WeaponSlots(deque):
	def __init__(self, limit):
		super().__init__()
		self.limit = limit

	def add_weapon(self, weapon):
		if len(self) < self.limit:
			self.appendleft(weapon)

	def change_weapon(self, new_weapon):
		self[0] = new_weapon

	def delete_weapon(self):
		if self:
			self.popleft()

	def scroll(self):
		self.rotate(-1)


class Knight(BaseHero):
	def __init__(self):
		super().__init__('knight', hp=5, protection=5, weapon_limit=2)