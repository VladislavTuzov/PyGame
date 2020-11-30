import pygame

from classes import Floor, Hero
import helpers

from config import FPS


def main():
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption('Hero movement')
	clock = pygame.time.Clock()

	floor = Floor(5, 5, 'dungeon')
	hero = Hero()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					hero.change_direction(x_shift, y_shift)
			elif event.type == pygame.KEYUP:
				if event.key in helpers.MOVEMENT_KEYS:
					x_shift, y_shift = handle_movement(event)
					hero.change_direction(-x_shift, -y_shift)

		hero.move()

		screen.fill((0, 0, 0))

		screen.blit(floor.image, floor.rect)
		screen.blit(hero.image, hero.rect)

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