import pygame

from classes import Floor, Knight
import helpers

from config import FPS


def main():
	screen_size = screen_width, screen_height = 600, 400
	# screen = pygame.display.set_mode(screen_size)
	screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
	pygame.display.set_caption('Hero movement')
	clock = pygame.time.Clock()

	floor = Floor(48, 24, 'dungeon')
	knight = Knight()

	running = True
	while running:

		for event in pygame.event.get():
			if (event.type == pygame.QUIT or 
					event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

			elif event.type == pygame.KEYDOWN:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					knight.change_direction(x_shift, y_shift)

			elif event.type == pygame.KEYUP:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					knight.change_direction(-x_shift, -y_shift)

		knight.move()

		screen.fill((0, 0, 0))

		screen.blit(floor.image, floor.rect)
		screen.blit(knight.image, knight.rect)

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