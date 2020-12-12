import pygame
import sys

from config import FPS
from classes import MenuButton
from classes import ExitPseudoError, NewGamePseudoError


def menu_screen(screen, cursor):
	pygame.mixer.music.load('source/music/menu.wav')

	clock = pygame.time.Clock()

	screen_rect = screen.get_rect()
	screen_width, screen_height = screen_rect.size

	new_game_button = MenuButton('new_game')
	new_game_button.rect.x = (screen_width - new_game_button.rect.width) // 2
	new_game_button.rect.y = screen_height // 2 - new_game_button.rect.height * 1.25

	continue_button = MenuButton('continue')
	continue_button.rect.x = (screen_width - continue_button.rect.width) // 2
	continue_button.rect.y = screen_height // 2 + continue_button.rect.height // 4

	home_button = MenuButton('home', x=300, y=300)
	settings_button = MenuButton('settings', x=400, y=400)
	exit_button = MenuButton('exit', x=500, y=500)

	pygame.mixer.music.play(loops=-1, fade_ms=10000)

	running = True
	while running:
		for event in pygame.event.get():
			if (event.type == pygame.QUIT
					or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				sys.exit(0)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if continue_button.collidepoint(event.pos):
					print('continue')
					pygame.mixer.music.fadeout(5000)
				elif new_game_button.collidepoint(event.pos):
					pygame.mixer.music.fadeout(5000)
					raise NewGamePseudoError('start new game')
				elif home_button.collidepoint(event.pos):
					print('home')
				elif settings_button.collidepoint(event.pos):
					print('settings')
				elif exit_button.collidepoint(event.pos):
					raise ExitPseudoError('exit from menu')

		screen.fill('black')

		screen.blit(new_game_button.image, new_game_button.rect)
		screen.blit(continue_button.image, continue_button.rect)
		screen.blit(home_button.image, home_button.rect)
		screen.blit(settings_button.image, settings_button.rect)
		screen.blit(exit_button.image, exit_button.rect)

		cursor.update_pos(pygame.mouse.get_pos())
		screen.blit(cursor.image, cursor.rect)

		pygame.display.flip()
		clock.tick(FPS)
