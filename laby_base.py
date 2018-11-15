import pygame, sys
from pygame.locals import *



pygame.init()

windowSurface = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Labyrinthe')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

i = 0
while i < 600:
    j = 0
    while j < 600:
        pygame.draw.rect(windowSurface, WHITE, (i, j, 40, 40))
        pygame.draw.rect(windowSurface, BLUE, (i , j+40, 40, 40))
        j = j + 80
    i = i + 80

i = 40
while i < 600:
    j = 0
    while j < 600:
        pygame.draw.rect(windowSurface, YELLOW, (i, j+40, 40, 40))
        pygame.draw.rect(windowSurface, BLUE, (i, j, 40, 40))
        j = j + 80
    i = i + 80


pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


# https://www.pygame.org/docs/ref/image.html
# https://www.pygame.org/docs/ref/key.html
# placer MacGyver, Murdock et murs sur la carte, faire que Mac puisse se déplacer avec les touches
# bonus : vérifier les collisions donc la position de Mac et voir si avec déplacement on tombe sur mur (avec double indice
# entre crochets)
