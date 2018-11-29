import pygame, sys
from pygame.locals import *
from parse import parse
from square import Square
from macgyver import Macgyver
from loot import Loot
import random
from murdock import Murdock
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
    """Create a list of unoccupied cases"""
    way = []
    i = 0
    while i < 15:
        j = 0
        while j < 15:
            case = Square(i, j, maze[i][j])
            value_case = case.name
            if value_case == " ":
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

# importation des images
img_mur = pygame.image.load("wall.png")
img_sol = pygame.image.load("ground.png")
img_murd = pygame.image.load("murd.png")
img_macgyver = pygame.image.load("macg.png")
img_needle = pygame.image.load("needle.png")
inv_needle = pygame.image.load("needle_loot.png")
img_tube = pygame.image.load("tube.png")
inv_tube = pygame.image.load("tube_loot.png")
img_ether = pygame.image.load("ether.png")
inv_ether = pygame.image.load("ether_loot.png")
screen_win = pygame.image.load("screen_win.png")
screen_lose = pygame.image.load("screen_lose.png")

pygame.mixer.music.load("bonk.wav")  # importation du son de collision

murdock = Murdock(520, 560, "murdock") # création de l'objet Murdock


def draw_laby():
    """Draws the labyrinth from the list created from maze.txt"""
    i = 0
    while i < 600:  # boucle de couleur des cases selon valeur name de maze
        j = 0
        while j < 600:
            case = Square(i // 40, j // 40, maze[i // 40][j // 40])
            value_case = case.name

            if value_case == "x":
                windowSurface.blit(img_mur, (case.x*40, case.y*40))
            elif value_case == " ":
                windowSurface.blit(img_sol, (case.x * 40, case.y * 40))
            elif value_case == "m":
                windowSurface.blit(img_sol, (case.x * 40, case.y * 40))
            else:
                windowSurface.blit(img_murd, (murdock.x, murdock.y))
            j = j + 40
        i = i + 40


pos_macgyver = Macgyver(520, 40, "m")  # création de l'objet MacG

objets = random.sample(way(), 3)  # prend 3 positions dans la liste de cases vides créée par la fonction way()

needle = objets[0]  # l'aiguille est le premier objet de la liste random
pos_needle = Loot(needle.x*40, needle.y*40, "needle")  # création de l'objet needle

tube = objets[1]  # le tube est le deuxième objet de la liste random
pos_tube = Loot(tube.x*40, tube.y*40, "tube")  # création de l'objet tube

ether = objets[2]  # l'ether est le troisième objet de la liste random
pos_ether = Loot(ether.x*40, ether.y*40, "ether")  # création de l'objet ether

win = False
lose = False

while 1:
    for event in pygame.event.get():

        # déplacement
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:  # si flèche gauche
                if maze[pos_macgyver.x//40 - 1][pos_macgyver.y//40] == " ":
                    pos_macgyver.x = pos_macgyver.x - 40  # se déplace vers la gauche
                else:
                    pygame.mixer.music.play()
            elif event.key == pygame.K_UP:  # si flèche haut
                if maze[pos_macgyver.x//40][pos_macgyver.y//40 - 1] == " ":
                    pos_macgyver.y = pos_macgyver.y - 40  # se déplace vers le haut
                else:
                    pygame.mixer.music.play()
            elif event.key == pygame.K_RIGHT:  # si flèche droite
                if maze[pos_macgyver.x//40 + 1][pos_macgyver.y//40] == " ":
                    pos_macgyver.x = pos_macgyver.x + 40  # se déplace vers la droite
                else:
                    pygame.mixer.music.play()
            elif event.key == pygame.K_DOWN:  # si flèche bas
                if maze[pos_macgyver.x//40][pos_macgyver.y//40 + 1] == " " or maze[pos_macgyver.x//40][pos_macgyver.y//40 + 1] == "v":
                    pos_macgyver.y = pos_macgyver.y + 40  # se déplace vers le bas
                else:
                    pygame.mixer.music.play()  # joue le bruit de collision
            else:
                pass

        # loot des objets
        if pos_macgyver.x == pos_needle.x and pos_macgyver.y == pos_needle.y:  # si MacG arrive sur l'aiguille
            pos_needle.picked = True
            pos_macgyver.loot[0] = True
        if pos_macgyver.x == pos_tube.x and pos_macgyver.y == pos_tube.y:  # si MacG arrive sur le tube
            pos_tube.picked = True
            pos_macgyver.loot[1] = True
        if pos_macgyver.x == pos_ether.x and pos_macgyver.y == pos_ether.y:  # si MacG arrive sur l'ether
            pos_ether.picked = True
            pos_macgyver.loot[2] = True

        # fin du jeu
        if pos_macgyver.x == murdock.x and pos_macgyver.y == murdock.y:  # MacG arrive sur Murdock
            if pos_macgyver.loot[0] and pos_macgyver.loot[1] and pos_macgyver.loot[2]:
                win = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # relance le jeu
                        # regrouper toutes ces conditions dans un truc "conditions initiales"
                        win = False
                        lose = False
                        pos_needle.picked = False
                        pos_macgyver.loot[0] = False
                        pos_tube.picked = False
                        pos_macgyver.loot[1] = False
                        pos_ether.picked = False
                        pos_macgyver.loot[2] = False
                        pos_macgyver = Macgyver(520, 40, "m")
                        # coordonnées aléatoires des loots
                    if event.key == pygame.K_a:
                        sys.exit()
                    else:
                        pass
            else:
                lose = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # relance le jeu
                        # regrouper toutes ces conditions dans un truc "conditions initiales"
                        win = False
                        lose = False
                        pos_needle.picked = False
                        pos_macgyver.loot[0] = False
                        pos_tube.picked = False
                        pos_macgyver.loot[1] = False
                        pos_ether.picked = False
                        pos_macgyver.loot[2] = False
                        pos_macgyver = Macgyver(520, 40, "m")
                        # coordonnées aléatoires des loots
                    if event.key == pygame.K_a:
                        sys.exit()
                    else:
                        pass
        if event.type == pygame.QUIT:
            sys.exit()

    # commencer cours P4 ou revoir code
    # préparer papier de soutenance

    draw_laby()
    windowSurface.blit(img_macgyver, (pos_macgyver.x, pos_macgyver.y))
    if pos_needle.picked == False:
        windowSurface.blit(img_needle, (pos_needle.x, pos_needle.y))  # affiche l'aiguille dans le labyrinthe
    else:
        windowSurface.blit(inv_needle, (0, 0))  # affiche l'aiguille dans l'inventaire
    if pos_tube.picked == False:
        windowSurface.blit(img_tube, (pos_tube.x, pos_tube.y))  # affiche le tube dans le labyrinthe
    else:
        windowSurface.blit(inv_tube, (0, 40))  # affiche le tube dans l'inventaire
    if pos_ether.picked == False:
        windowSurface.blit(img_ether, (pos_ether.x, pos_ether.y))  # affiche l'ether dans le labyrinthe
    else:
        windowSurface.blit(inv_ether, (0, 80))  # affiche l'ether dans l'inventaire
    if win == True:
        windowSurface.blit(screen_win, (0, 0))  # affiche l'écran de victoire
    if lose == True:
        windowSurface.blit(screen_lose, (0, 0))  # affiche l'écran de défaite
    pygame.display.update()
