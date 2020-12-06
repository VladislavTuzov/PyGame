import pygame

from classes import Room, Knight, Dardo, Weapon
from classes import MenuButton, CustomCursor
from config import FPS
import helpers


def test_hero():
	screen_size = screen_width, screen_height = 1366, 768
	screen = pygame.display.set_mode(screen_size,
									 flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED)
	# pygame.display.set_mode(screen_size)
	# screen = Surface(1366, 768)
	pygame.display.set_caption('Hero Test')

	clock = pygame.time.Clock()
	pygame.mouse.set_visible(False)
	cursor = CustomCursor('cursor20alt.png')

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
	knight.add_weapon(Weapon('broom', damage=1, cooldown=0.1))
	knight.add_weapon(Weapon('awp', damage=5, cooldown=2))
	bullets = pygame.sprite.Group()

	enemies = helpers.RectGroup()
	enemy = Dardo()
	enemy.rect.center = (100, 100)
	enemies.add(enemy)

	mouse_pressed = False
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
				elif event.key == helpers.WEAPON_SCROLL:
					knight.scroll()

			elif event.type == pygame.KEYUP:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					knight.change_direction(-x_shift, -y_shift)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pressed = True
				pos = event.pos
				bullet = knight.shoot(pos)
				if bullet:
					bullets.add(bullet)

			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_pressed = False

		knight.move(room.walls)
		if mouse_pressed:
			pos = pygame.mouse.get_pos()
			bullet = knight.shoot(pos)
			if bullet:
				bullets.add(bullet)

		screen.fill('black')

		screen.blit(room.image, room.rect)
		screen.blit(knight.image, knight.rect)
		screen.blit(knight.weapon.image, knight.weapon.rect)
		
		enemies.update()
		enemies.draw(screen)

		bullets.update(room.walls, enemies)
		bullets.draw(screen)

		cursor.update_pos(pygame.mouse.get_pos())
		screen.blit(cursor.image, cursor.rect)

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
	pygame.mixer.music.load('source/music/menu.wav')

	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
	pygame.display.set_caption('Menu Test')
	clock = pygame.time.Clock()

	screen_rect = screen.get_rect()
	screen_width, screen_height = screen_rect.width, screen_rect.height

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
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if continue_button.collidepoint(event.pos):
					print('continue')
					pygame.mixer.music.fadeout(5000)
				elif new_game_button.collidepoint(event.pos):
					print('new_game')
					pygame.mixer.music.fadeout(5000)
				elif home_button.collidepoint(event.pos):
					print('home')
				elif settings_button.collidepoint(event.pos):
					print('settings')
				elif exit_button.collidepoint(event.pos):
					print('exit')
					running = False

		screen.fill('black')

		screen.blit(new_game_button.image, new_game_button.rect)
		screen.blit(continue_button.image, continue_button.rect)
		screen.blit(home_button.image, home_button.rect)
		screen.blit(settings_button.image, settings_button.rect)
		screen.blit(exit_button.image, exit_button.rect)

		screen = pygame.transform.scale(screen, screen_size)

		pygame.display.flip()
		clock.tick(FPS)


if __name__ == '__main__':
	pygame.init()
	test_hero()
	pygame.quit()
