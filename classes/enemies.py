from math import hypot, atan2, cos, sin

import pygame

from config import FPS
from classes.weapons import Staff


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, name, hp, points_cost=1000):
        super().__init__()
        self.image_right = pygame.image.load(f'source/enemies/{name}.png')
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image = self.image_left
        self.rect = self.image.get_rect()

        self.hp = hp
        self.speed = 180 / FPS
        self.points_cost = points_cost

    def hit(self, bullet, points):
        self.hp -= bullet.damage
        if self.hp <= 0:
            self.kill()
            points += self.points_cost

    def shoot(self, target, bullets):
        bullet = self.weapon.shoot(target)
        if bullet:
            bullets.add(bullet)

    def update(self, hero):
        x0, y0 = self.rect.center
        x1, y1 = hero.rect.center

        if x0 < x1:
            self.image = self.image_right
            self.weapon.change_direction(1)
        else:
            self.image = self.image_left
            self.weapon.change_direction(-1)

        x_dist = x1 - x0
        y_dist = y1 - y0
        dist = hypot(x_dist, y_dist)

        if dist >= 150:
            coeff = atan2(y_dist, x_dist)
            self.rect.x += self.speed * round(cos(coeff), 1)
            self.rect.y += self.speed * round(sin(coeff), 1)

        self.weapon.rect.center = self.rect.center


class Dardo(BaseEnemy):
    def __init__(self):
        super().__init__('dardo', hp=3)
        self.weapon = Staff()
        # self.weapon.change_direction()
