from collections import deque

import pygame

from config import FPS
from classes.exceptions import HeroDeath


class BaseHero(pygame.sprite.Sprite):
    def __init__(self, hero_name, hp, protection, weapon_limit=2):
        super().__init__()
        # pygame attributes
        self.load_sheet(hero_name)

        self.image = self.currect_frames[0]  # start direction - left
        self.rect = self.image.get_rect()

        self.speed = 270 / FPS  # pixels per second
        self.direction = [0, 0]

        self.x_direction = 0  # help us to rotate weapon when scrolling

        # gameplay attributes
        self.hp = hp
        self.stamina = 100
        self.protection = protection
        self.weapons = WeaponSlots(weapon_limit)

        self.is_acceleration = False

    def load_sheet(self, hero_name):
        self.left_frames = deque()
        self.cut_sheet(hero_name, 4, 1)

        self.right_frames = deque([
            pygame.transform.flip(frame, True, False)
            for frame in self.left_frames
        ])

        self.currect_frames = self.left_frames

    def cut_sheet(self, hero_name, cols, rows):
        sheet = pygame.image.load(f'source/heroes/{hero_name}/default.png')
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // cols, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(cols):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame = sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size))
                self.left_frames.extendleft([frame] * 15)

    def change_direction(self, x_vector_change, y_vector_change):
        self.direction[0] += x_vector_change
        self.direction[1] += y_vector_change

        if self.direction[0] == -1:
            self.currect_frames = self.left_frames
        elif self.direction[0] == 1:
            self.currect_frames = self.right_frames
            
        self.image = self.currect_frames[0]
        self.weapon.change_direction(self.direction[0])

        self.x_direction = self.direction[0] or self.x_direction

    def update_image(self):
        self.left_frames.rotate()
        self.right_frames.rotate()
        self.image = self.currect_frames[0]

    def set_acceleration(self, value):
        if self.stamina >= 100:
            self.is_acceleration = value
        else:
            self.is_acceleration = False

    def move(self, walls):
        if self.is_acceleration and self.stamina > 0:
            speed_coeff = 2
            self.stamina -= 50 / FPS
        else:
            speed_coeff = 1
            if self.stamina < 100:
                self.stamina += 25 / FPS

        x = self.rect.centerx + self.direction[0] * self.speed * speed_coeff
        y = self.rect.centery + self.direction[1] * self.speed * speed_coeff

        prev_center = self.rect.center
        self.rect.centerx = x
        if self.rect.collidelist(walls) != -1:
            self.rect.center = prev_center

        prev_center = self.rect.center
        self.rect.centery = y
        if self.rect.collidelist(walls) != -1:
            self.rect.center = prev_center

        self.weapon.rect.center = (self.rect.centerx, self.rect.centery + 10)

    def hit(self, bullet):
        self.hp -= bullet.damage
        if self.hp <= 0:
            raise HeroDeath("Game over")

    def shoot(self, target, bullets):
        bullet = self.weapon.shoot(target)
        if bullet:
            bullets.add(bullet)

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
        self.weapon.change_direction(self.x_direction)


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
