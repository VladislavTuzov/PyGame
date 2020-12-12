import pygame

import gameplay
import menu

import config
from classes.heroes import Knight
from classes.weapons import BaseWeapon, Broom
from classes.interface import CustomCursor
from classes.exceptions import ExitPseudoError, NewGamePseudoError
import helpers


def main():
	screen_size = screen_width, screen_height = 1366, 768
	screen = pygame.display.set_mode(screen_size,
									 flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
	pygame.display.set_caption('Game')

	pygame.mouse.set_visible(False)
	cursor = CustomCursor(config.CURSOR_FILENAME)

	knight = Knight()
	knight.add_weapon(BaseWeapon('awp', damage=5, cooldown=2))
	knight.add_weapon(Broom())

	try:
		menu.menu_screen(screen, cursor)
	except NewGamePseudoError:
		gameplay.play_level(screen, cursor, knight)
	except ExitPseudoError:
		pass


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()
