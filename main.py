import os
import pygame

from classes import Room, Knight, MenuButton, Dardo
from config import FPS
import helpers

cursor_image = pygame.image.load('cursor.png')
cursor_rect = cursor_image.get_rect()


def test_hero():
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
	pygame.display.set_caption('Hero Test')
	clock = pygame.time.Clock()

	pattern = ('  WWWWWWWWWWWWWW',
			   '               W',
			   '               W',
			   '               W',
			   '        W      W',
			   '       WWW     W',
			   '         W     W',
			   '      WWW      W',
			   '               W',
			   'W       W      W',
			   'WWW          WWW',)

	room = Room(pattern, 'dungeon')
	knight = Knight()
	enemy = Dardo()
	enemy.rect.center = (100, 100)

	running = True
	while running:

		for event in pygame.event.get():
			if (event.type == pygame.QUIT
					or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

			elif event.type == pygame.KEYDOWN:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					knight.change_direction(x_shift, y_shift)

			elif event.type == pygame.KEYUP:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					knight.change_direction(-x_shift, -y_shift)

		knight.move(room.walls)

		screen.fill((0, 0, 0))

		screen.blit(room.image, room.rect)
		screen.blit(knight.image, knight.rect)
		screen.blit(enemy.image, enemy.rect)

		mouse_pos = pygame.mouse.get_pos()
		cursor_rect.center = mouse_pos
		screen.blit(cursor_image, cursor_rect)

		pygame.display.flip()
		clock.tick(FPS)


def handle_movement(event):
	if event.key == helpers.UP:
		x_shift, y_shift = 0, -1
	elif event.key == helpers.LEFT:
		x_shift, y_shift = -1, 0
	elif event.key == helpers.DOWN:
		x_shift, y_shift = 0, +1
	elif event.key == helpers.RIGHT:
		x_shift, y_shift = +1, 0
	return x_shift, y_shift


def test_menu():
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
	pygame.display.set_caption('Menu Test')
	clock = pygame.time.Clock()

	new_game_button = MenuButton('new_game', x=100, y=100)
	continue_button = MenuButton('continue', x=200, y=200)
	home_button = MenuButton('home', x=300, y=300)
	settings_button = MenuButton('settings', x=400, y=400)
	exit_button = MenuButton('exit', x=500, y=500)

	running = True
	while running:
		for event in pygame.event.get():
			if (event.type == pygame.QUIT
					or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if continue_button.collidepoint(event.pos):
					print('continue')
				elif new_game_button.collidepoint(event.pos):
					print('new_game')
				elif home_button.collidepoint(event.pos):
					print('home')
				elif settings_button.collidepoint(event.pos):
					print('settings')
				elif exit_button.collidepoint(event.pos):
					print('exit')
					running = False

		screen.fill((123, 123, 123))

		screen.blit(new_game_button.image, new_game_button.rect)
		screen.blit(continue_button.image, continue_button.rect)
		screen.blit(home_button.image, home_button.rect)
		screen.blit(settings_button.image, settings_button.rect)
		screen.blit(exit_button.image, exit_button.rect)

		pygame.display.flip()
		clock.tick(FPS)


if __name__ == '__main__':
	pygame.init()
	pygame.mouse.set_visible(False)
	test_hero()
	pygame.quit()
