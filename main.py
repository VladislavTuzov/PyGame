import pygame

pygame.init()
pygame.display.set_caption('game')
screen = pygame.display.set_mode((600, 400))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    pygame.display.flip()

pygame.quit()
