import pygame

from classes import Floor


def main():
	width, height = 600, 400
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Floor')

	floor = Floor(4, 3, 'dungeon')

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.fill((0, 0, 0))
		screen.blit(floor.image, floor.rect)
		pygame.display.flip()


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()