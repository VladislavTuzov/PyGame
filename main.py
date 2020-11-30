import pygame

from classes import Floor, Hero
import helpers


def main():
	width, height = 600, 400
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Floor')

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
					hero.move(x_shift, y_shift)

		screen.fill((0, 0, 0))

		screen.blit(floor.image, floor.rect)
		screen.blit(hero.image, hero.rect)

		pygame.display.flip()


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