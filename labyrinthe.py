import pygame, sys
from pygame.locals import *
from parse import parse
from carre import Square
from macgyver import Macgyver
from loot import Loot
import random
from map import Map


laby = open("maze.txt", "r")  # ouverture du fichier maze.txt
contenu = laby.read()  # renvoie le contenu du fichier

maze = []  # création de la liste finale du laby (= list_valid)
maze_list = []  # création de la liste de liste de ligne (= map)
maze_str = contenu.splitlines()  # séparation de chaque ligne du fichier en liste de chaines de caractères


for line in maze_str:
    maze_list.append(parse(line))  # on parse chaque ligne de caractère pour avoir une liste de listes

for line in maze_list:
    maze.append(parse(line))  # on parse chaque liste de listes


def way():
    way = []
    i = 0
    while i < 15:
        j = 0
        while j < 15:
            case = Square(i, j, maze[i][j])
            valeur_case = case.name
            if valeur_case == " ":
                way.append(case)
            j = j + 1
        i = i + 1
    return way


pygame.init()

windowSurface = pygame.display.set_mode((600, 600), 0, 32)  # fenêtre de 600x600 px
pygame.display.set_caption('Labyrinthe')  # nommée Labyrinthe

# définition des couleurs

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

img_mur = pygame.image.load("mur.png")
img_sol = pygame.image.load("sol.png")
img_murd = pygame.image.load("murd.png")

def draw_laby():
    i = 0
    while i < 600:  # boucle de couleur des cases selon valeur name de maze (remplacer plus tard par une image, cf pygame.Surface.blit)
        j = 0
        while j < 600:
            case = Square(i // 40, j // 40, maze[i // 40][j // 40])
            valeur_case = case.name

            if valeur_case == "x":
                windowSurface.blit(img_mur, (case.x*40, case.y*40))
            elif valeur_case == " ":
                windowSurface.blit(img_sol, (case.x * 40, case.y * 40))
            #elif valeur_case == "m":
                #color = BLUE
            else:
                windowSurface.blit(img_murd, (case.x * 40, case.y * 40))
            #pygame.draw.rect(windowSurface, color, (i, j, 40, 40))
            j = j + 40
        i = i + 40


# définir pos_macgyver depuis case avec "m" dans maze


pos_macgyver = Macgyver (520, 40, "m")  # position directe de mac, mais pas récupérée de maze
img_macgyver = pygame.image.load("macg.png")

objets = random.sample(way(), 3)  #isoler les cases libres

needle = objets[0]
pos_needle = Loot(needle.x*40, needle.y*40, "o")
img_needle = pygame.image.load("needle.png")

tube = objets[1]
pos_tube = Loot(tube.x*40, tube.y*40, "o")
img_tube = pygame.image.load("tube.png")

ether = objets[2]
pos_ether = Loot(ether.x*40, ether.y*40, "o")
img_ether = pygame.image.load("ether.png")


while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:  # si flèche gauche
                if maze[pos_macgyver.x//40 - 1][pos_macgyver.y//40] == " ":
                    pos_macgyver.x = pos_macgyver.x - 40  # se déplace vers la gauche
            elif event.key == pygame.K_UP:  # si flèche haut
                if maze[pos_macgyver.x//40][pos_macgyver.y//40 - 1] == " ":
                    pos_macgyver.y = pos_macgyver.y - 40  # se déplace vers le haut
            elif  event.key == pygame.K_RIGHT:  # si flèche droite
                if maze[pos_macgyver.x//40 + 1][pos_macgyver.y//40] == " ":
                    pos_macgyver.x = pos_macgyver.x + 40  # se déplace vers la droite
            elif  event.key == pygame.K_DOWN:  # si flèche bas
                if maze[pos_macgyver.x//40][pos_macgyver.y//40 + 1] == " ":
                    pos_macgyver.y = pos_macgyver.y + 40  # se déplace vers le bas
            else:
                pass
        if event.type == pygame.QUIT:
            sys.exit()


    # print(str(pos_macgyver.x) + " " + str(pos_macgyver.y))

    # pygame.Surface.blit pour dessiner une image sur une autre (avec Surface((40, 40)) ?), l'utiliser à un moment pour
    # mettre des textures sur le labyrinthe, selon la valeur de la lettre des coord dans maze

    draw_laby()
    windowSurface.blit(img_needle, (pos_needle.x, pos_needle.y))
    windowSurface.blit(img_tube, (pos_tube.x, pos_tube.y))
    windowSurface.blit(img_ether, (pos_ether.x, pos_ether.y))
    windowSurface.blit(img_macgyver, (pos_macgyver.x, pos_macgyver.y))
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

# objets qui apparaissent à looter