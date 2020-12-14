import pygame


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
