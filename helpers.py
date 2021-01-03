import pygame


# KEYS

MOVEMENT_KEYS = (
    pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
    pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT
)


class CombinedKey:
    '''
    Combine two or more keys into one.
    Example: W and UP_ARROW -> UP
    '''
    def __init__(self, *keys):
        self.keys = keys

    def __eq__(self, key):
        return key in self.keys


UP    = CombinedKey(pygame.K_w, pygame.K_UP)
DOWN  = CombinedKey(pygame.K_s, pygame.K_DOWN)
LEFT  = CombinedKey(pygame.K_a, pygame.K_LEFT)
RIGHT = CombinedKey(pygame.K_d, pygame.K_RIGHT)


WEAPON_SCROLL = pygame.K_TAB
INTERACTION   = pygame.K_SPACE

# ROOM GENERATION

PORTAL = "P"
SPAWN  = "S"
ROOM   = "#"
BOSS   = "B"
V_TUNN = "|"
H_TUNN = "-"
ROOMS   = (PORTAL, SPAWN, ROOM)
TUNNELS = (V_TUNN, H_TUNN)

WALL  = "W"
FLOOR = " "
GATES = "G"
BIRTH = "B"
ENEMY = "E"


class EnemiesGroup(pygame.sprite.Group):
    """
    Group for enemies and their methods
    """
    def collidesprite(self, sprite):
        return pygame.sprite.spritecollide(sprite, self, dokill=False)

    def shoot(self, target, bullets):
        for enemy in self:
            enemy.shoot(target, bullets)

    def draw_weapons(self, screen):
        for enemy in self:
            screen.blit(enemy.weapon.image, enemy.weapon.rect)


class InteractionGroup(pygame.sprite.Group):
    """
    Pygame's Group but with interact method.
    Was made for check player interact with objects
    """
    def interact(self, hero):
        for sprite in self:
            sprite.interact(hero)


class EnemiesBullets(pygame.sprite.Group):
    """
    Group of enemies bullets for call
    update_as_enemies Bullet's method
    """
    def update_as_enemies(self, walls, target):
        for bullet in self:
            bullet.update_as_enemies(walls, target)


class Points:
    """
    Hidden subclass of int that we can mutable everywhere,
    so we musn't return it from functions like default int
    """
    def __init__(self, value=0):
        self.value = value

    def __iadd__(self, other):
        self.value += other
        return self

    def __str__(self):
        return str(self.value)
