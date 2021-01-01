import pygame

# before import our modules we need to initialize
# pygame.mixer because weapons in classes/weapons
# use him for their shooting sounds
pygame.mixer.init()

import gameplay
import menu

import config
from classes.heroes import Knight
from classes.weapons import *
from classes.interface import CustomCursor
from classes.exceptions import ExitPseudoError, NewGamePseudoError


def main():
    pygame.init()

    screen = pygame.display.set_mode(config.SCREEN_SIZE,
                flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
    font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)
    pygame.display.set_caption('Game')

    hero = Knight()
    hero.add_weapon(AWP())
    hero.add_weapon(Broom())

    try:
        menu.menu_screen(screen)
    except NewGamePseudoError:
        pygame.mouse.set_visible(False)
        cursor = CustomCursor(config.CURSOR_FILENAME)
        gameplay.play_level(screen, font, cursor, hero)
    except ExitPseudoError:
        pass

    pygame.quit()


if __name__ == '__main__':
    main()
