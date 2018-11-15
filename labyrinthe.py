import pygame, sys
from pygame.locals import *
from parse import parse
from carre import Square

laby = open("maze.txt", "r")  # ouverture du fichier maze.txt
contenu = laby.read()  # renvoie le contenu du fichier

maze = []  # création de la liste finale du laby (= list_valid)
maze_list = []  # création de la liste de liste de ligne (= map)
maze_str = contenu.splitlines()  # séparation de chaque ligne du fichier en liste de chaines de caractères

for line in maze_str:
    maze_list.append(parse(line))  # on parse chaque ligne de caractère pour avoir une liste de listes

for line in maze_list:
    maze.append(parse(line))  # on parse chaque liste de listes


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
        case = Square(j // 40, i // 40, maze[j // 40][i // 40])
        valeur_case = case.name

        if valeur_case == "x":
            color = BLACK
        elif valeur_case == " ":
            color = WHITE
        elif valeur_case == "m":
            color = BLUE
        else:
            color = RED
        pygame.draw.rect(windowSurface, color, (i, j, 40, 40))
        j = j + 40
    i = i + 40


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