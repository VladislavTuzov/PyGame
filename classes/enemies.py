import pygame


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
