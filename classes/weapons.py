from math import hypot
from time import time

import pygame

from config import FPS


class BaseWeapon(pygame.sprite.Sprite):
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
			return BaseBullet(
						self.weapon_name,
						self.rect.center,
						pos,
						speed=420,
						damage=self.damage
				   )


class BaseBullet(pygame.sprite.Sprite):
	def __init__(self, weapon_name, start, pos, speed, damage, max_distance=2000):
		super().__init__()
		self.image = pygame.image.load(f'source/weapons/{weapon_name}/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = start

		self.speed = speed / FPS  # pixels by second
		self.damage = damage
		self.max_distance = max_distance

		self.x0, self.y0 = start
		x1, y1 = pos
		self.current_distance = 0
		self.x_distance = x1 - self.x0
		self.y_distance = y1 - self.y0
		self.target_distance = hypot(self.x_distance, self.y_distance)

	def update(self, walls, enemies):
		self.current_distance += self.speed
		if self.current_distance >= self.max_distance:
			self.kill()
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


class Broom(BaseWeapon):
	def __init__(self):
		super().__init__('broom', 1, 0.2)

	def shoot(self, pos):
		shot_time = time()
		if shot_time - self.previous_shot_time >= self.cooldown:
			self.previous_shot_time = shot_time
			return BroomBullet(
						self.weapon_name,
						self.rect.center,
						pos,
						speed=420,
						damage=self.damage
				   )


class BroomBullet(BaseBullet):
	pass