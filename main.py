import os
import pygame

from classes import Floor, Knight, MenuBtn
import helpers

from config import FPS


# def main():
# 	screen_size = screen_width, screen_height = 600, 400
# 	# screen = pygame.display.set_mode(screen_size)
# 	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# 	pygame.display.set_caption('Hero movement')
# 	clock = pygame.time.Clock()

# 	floor = Floor(24, 12, 'dungeon')
# 	knight = Knight()

# 	running = True
# 	while running:

# 		for event in pygame.event.get():
# 			if (event.type == pygame.QUIT or
# 					event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
# 				running = False

# 			elif event.type == pygame.KEYDOWN:
# 				if event.key in helpers.MOVEMENT_KEYS:
# 					x_shift, y_shift = handle_movement(event)
# 					knight.change_direction(x_shift, y_shift)

# 			elif event.type == pygame.KEYUP:
# 				if event.key in helpers.MOVEMENT_KEYS:
# 					x_shift, y_shift = handle_movement(event)
# 					knight.change_direction(-x_shift, -y_shift)

# 		knight.move()

# 		screen.fill((0, 0, 0))

# 		screen.blit(floor.image, floor.rect)
# 		screen.blit(knight.image, knight.rect)

# 		pygame.display.flip()
# 		clock.tick(FPS)


def main():
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
	pygame.display.set_caption('Hero movement')
	clock = pygame.time.Clock()
	running = True

	while running:
		btn_continue = pygame.image.load(f'source/buttons/new_game.png')
		btn_new_game = pygame.image.load(f'source/buttons/icon_continue.png')
		btn_settings = pygame.image.load(f'source/buttons/icon_settings.png')
		btn_exit = pygame.image.load(f'source/buttons/icon_exit.png')
		btn_settings = pygame.transform.scale(btn_settings, (60, 60))
		btn_exit = pygame.transform.scale(btn_exit, (60, 60))
		btn_rect_continue = pygame.draw.rect(
			screen, "red", (400, 650, 528, 714))
		btn_rect_new_game = pygame.draw.rect(
			screen, "red", (800, 650, 928, 714))
		btn_rect_settings = pygame.draw.rect(
			screen, "red", (600, 650, 664, 714))
		btn_rect_exit = pygame.draw.rect(
			screen, "red", (200, 650, 264, 714))
		for event in pygame.event.get():
			if (event.type == pygame.QUIT or
					event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_rect_continue.collidepoint(event.pos):
					print('continue')

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_rect_new_game.collidepoint(event.pos):
					print('new_game')

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_rect_settings.collidepoint(event.pos):
					print('settings')

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_rect_exit.collidepoint(event.pos):
					running = False

		screen.fill((123, 123, 123))
		screen.blit(btn_continue, (400, 650))
		screen.blit(btn_new_game, (800, 650))
		screen.blit(btn_settings, (630, 655))
		screen.blit(btn_exit, (200, 655))

		# screen.blit(floor.image, floor.rect)
		# screen.blit(knight.image, knight.rect)

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


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()
