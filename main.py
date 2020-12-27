import pygame

import gameplay
import menu

import config
from classes.heroes import Knight
from classes.weapons import BaseWeapon, Broom
from classes.interface import CustomCursor
from classes.exceptions import ExitPseudoError, NewGamePseudoError


def main():
    pygame.init()

    screen = pygame.display.set_mode(config.SCREEN_SIZE,
                flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
    pygame.display.set_caption('Game')

    hero = Knight()
    hero.add_weapon(BaseWeapon('awp', damage=5, cooldown=2))
    hero.add_weapon(Broom())

    try:
        menu.menu_screen(screen)
    except NewGamePseudoError:
        pygame.mouse.set_visible(False)
        cursor = CustomCursor(config.CURSOR_FILENAME)
        gameplay.play_level(screen, cursor, hero)
    except ExitPseudoError:
        pass

    pygame.quit()


if __name__ == '__main__':
    main()
