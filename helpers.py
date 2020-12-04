import pygame


# KEYS

MOVEMENT_KEYS = (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
				 pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)


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

# ROOM GENERATION

WALL  = 'W'
FLOOR = ' '


class RectList(list):
	def __init__(self):
		list.__init__(self)

	def colliderect(self, rect):
		return any(r.colliderect(rect) for r in self)


class RectGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

	def colliderect(self, rect):
		return [s for s in self if s.rect.colliderect(rect)]