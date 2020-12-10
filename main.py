import pygame

import gameplay
import menu

from classes import Knight, BaseWeapon, Broom
from classes import MenuButton, CustomCursor
from classes import MenuExitPseudoError
import helpers


def main():
	screen_size = screen_width, screen_height = 1366, 768
	screen = pygame.display.set_mode(screen_size,
									 flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
	pygame.display.set_caption('Hero Test')

	pygame.mouse.set_visible(False)
	cursor = CustomCursor('cursor20alt.png')

	knight = Knight()
	knight.add_weapon(Broom())
	knight.add_weapon(BaseWeapon('awp', damage=5, cooldown=2))

	try:
		menu.menu_screen(screen, cursor)
	except MenuExitPseudoError:
		pass
	gameplay.play_level(screen, cursor, knight)


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()
