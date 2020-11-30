import pygame


MOVEMENT_KEYS = (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
				 pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)


class CombinedKey:
	'''
	Combine two or more keys into one.
	Example: W and LEFT_ARROW -> LEFT
	'''
	def __init__(self, *keys):
		self.keys = keys

	def __eq__(self, key):
		return key in self.keys


UP = CombinedKey(pygame.K_w, pygame.K_UP)
DOWN = CombinedKey(pygame.K_s, pygame.K_DOWN)
LEFT = CombinedKey(pygame.K_a, pygame.K_LEFT)
RIGHT = CombinedKey(pygame.K_d, pygame.K_RIGHT)