from math import hypot
from time import time

import pygame

from config import FPS, SOUND_VOLUME


class BaseWeapon(pygame.sprite.Sprite):
    def __init__(self, weapon_name, cooldown):
        super().__init__()

        self.image_right = pygame.image.load(
            f'source/weapons/{weapon_name}/right.png')
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image = self.image_left  # start direction - left
        self.rect = self.image.get_rect()

        self.cooldown = cooldown
        self.previous_shot_time = time() - self.cooldown - 0.00001

    def change_direction(self, direction):
        if direction == -1:
            self.image = self.image_left
        elif direction == 1:
            self.image = self.image_right

    def shoot(self, target):
        shot_time = time()
        if shot_time - self.previous_shot_time >= self.cooldown:
            self.previous_shot_time = shot_time
            return self.bullet(start=self.rect.center, target=target)


class BaseBullet(pygame.sprite.Sprite):
    max_distance = 2000

    def __init__(self, start, target):
        super().__init__()

        self.rect = self.image.get_rect()
        self.rect.center = start

        self.shoot(start, target)

    def shoot(self, start, target):
        # attributes for flight calcutations
        self.current_distance = 0
        self.x0, self.y0 = start
        x1, y1 = target
        self.x_distance = x1 - self.x0
        self.y_distance = y1 - self.y0
        self.target_distance = hypot(self.x_distance, self.y_distance)

        self.play_sound()

    def play_sound(self):
        self.sound.set_volume(SOUND_VOLUME)
        self.sound.play()

    def update(self, walls, enemies, points):
        self.update_pos()

        if self.rect.collidelist(walls) != -1:
            self.kill()

        elif collided_enemies := enemies.collidesprite(self):
            enemy = collided_enemies[0]
            enemy.hit(self, points)
            self.kill()

    def update_as_enemies(self, walls, hero):
        self.update_pos()

        if self.rect.collidelist(walls) != -1:
            self.kill()

        elif pygame.sprite.collide_rect(self, hero):
            hero.hit(self)
            self.kill()

    def update_pos(self):
        self.current_distance += self.speed
        if self.current_distance >= self.max_distance:
            self.kill()
        coeff = self.current_distance / self.target_distance

        x = self.x0 + self.x_distance * coeff
        y = self.y0 + self.y_distance * coeff
        self.rect.center = (x, y)


class Broom(BaseWeapon):
    def __init__(self):
        super().__init__('broom', cooldown=0.2)
        self.bullet = BroomBullet


class BroomBullet(BaseBullet):
    image = pygame.image.load('source/weapons/broom/bullet.png')
    sound = pygame.mixer.Sound('source/weapons/broom/shot.wav')
    damage = 1
    speed = 420 / FPS


class AWP(BaseWeapon):
    def __init__(self):
        super().__init__('awp', cooldown=2)
        self.bullet = AWPBullet


class AWPBullet(BaseBullet):
    image = pygame.image.load('source/weapons/awp/bullet.png')
    sound = pygame.mixer.Sound('source/weapons/awp/shot.wav')
    damage = 5
    speed = 900 / FPS


class Staff(BaseWeapon):
    def __init__(self):
        super().__init__('staff', cooldown=1.5)
        self.bullet = StaffBullet


class StaffBullet(BaseBullet):
    image = pygame.image.load('source/weapons/staff/bullet.png')
    sound = pygame.mixer.Sound('source/weapons/staff/shot.wav')
    damage = 1
    speed = 280 / FPS
