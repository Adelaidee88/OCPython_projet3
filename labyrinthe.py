import pygame, sys
from pygame.locals import *
from parse import parse
from square import Square
from macgyver import Macgyver
from loot import Loot
import random
from murdock import Murdock
from map import Map


laby = open("maze.txt", "r")  # open file maze.txt
contenu = laby.read()  # return file content

maze = []  # création de la liste finale du laby
maze_list = []  # création de la liste de liste de ligne
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

windowSurface = pygame.display.set_mode((600, 600), 0, 32)  # window of 600x600 px
pygame.display.set_caption('Labyrinth')  # named Labyrinth

# colors definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# images loaded
img_mur = pygame.image.load("resources/wall.png")
img_sol = pygame.image.load("resources/ground.png")
img_murd = pygame.image.load("resources/murd.png")
img_macgyver = pygame.image.load("resources/macg.png")
img_needle = pygame.image.load("resources/needle.png")
inv_needle = pygame.image.load("resources/needle_loot.png")
img_tube = pygame.image.load("resources/tube.png")
inv_tube = pygame.image.load("resources/tube_loot.png")
img_ether = pygame.image.load("resources/ether.png")
inv_ether = pygame.image.load("resources/ether_loot.png")
screen_win = pygame.image.load("resources/screen_win.png")
screen_lose = pygame.image.load("resources/screen_lose.png")

pygame.mixer.music.load("resources/bonk.wav")  # collision sound loaded


def draw_laby():
    """Draws the labyrinth from the maze list created from maze.txt"""
    i = 0
    while i < 600:  # cases texture from name value of maze
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


macgyver = Macgyver(520, 40, "m")  # création de l'objet MacG
murdock = Murdock(520, 560, "murdock") # création de l'objet Murdock

objects = random.sample(way(), 3)  # prend 3 positions dans la liste de cases vides créée par la fonction way()

needle = objects[0]  # l'aiguille est le premier objet de la liste random
pos_needle = Loot(needle.x*40, needle.y*40, "needle")  # création de l'objet needle

tube = objects[1]  # le tube est le deuxième objet de la liste random
pos_tube = Loot(tube.x*40, tube.y*40, "tube")  # création de l'objet tube

ether = objects[2]  # l'ether est le troisième objet de la liste random
pos_ether = Loot(ether.x*40, ether.y*40, "ether")  # création de l'objet ether

win = False
lose = False
end = False

while 1:
    for event in pygame.event.get():

        # déplacement
        if end == False:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:  # si flèche gauche
                    if maze[macgyver.x//40 - 1][macgyver.y//40] == " ":
                        macgyver.x = macgyver.x - 40  # se déplace vers la gauche
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_UP:  # si flèche haut
                    if maze[macgyver.x//40][macgyver.y//40 - 1] == " ":
                        macgyver.y = macgyver.y - 40  # se déplace vers le haut
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_RIGHT:  # si flèche droite
                    if maze[macgyver.x//40 + 1][macgyver.y//40] == " ":
                        macgyver.x = macgyver.x + 40  # se déplace vers la droite
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_DOWN:  # si flèche bas
                    if maze[macgyver.x//40][macgyver.y//40 + 1] == " " or maze[macgyver.x//40][macgyver.y//40 + 1] == "v":
                        macgyver.y = macgyver.y + 40  # se déplace vers le bas
                    else:
                        pygame.mixer.music.play()  # joue le bruit de collision
                else:
                    pass

            # loot des objets
            if macgyver.x == pos_needle.x and macgyver.y == pos_needle.y:  # si MacG arrive sur l'aiguille
                pos_needle.picked = True
                macgyver.loot[0] = True
            if macgyver.x == pos_tube.x and macgyver.y == pos_tube.y:  # si MacG arrive sur le tube
                pos_tube.picked = True
                macgyver.loot[1] = True
            if macgyver.x == pos_ether.x and macgyver.y == pos_ether.y:  # si MacG arrive sur l'ether
                pos_ether.picked = True
                macgyver.loot[2] = True

        # fin du jeu
        if macgyver.x == murdock.x and macgyver.y == murdock.y:  # MacG arrive sur Murdock
            end = True
            if macgyver.loot[0] and macgyver.loot[1] and macgyver.loot[2]:
                win = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # relance le jeu
                        # regrouper toutes ces conditions dans un truc "conditions initiales"
                        win = False
                        lose = False
                        end = False
                        pos_needle.picked = False
                        macgyver.loot[0] = False
                        pos_tube.picked = False
                        macgyver.loot[1] = False
                        pos_ether.picked = False
                        macgyver.loot[2] = False
                        macgyver = Macgyver(520, 40, "m")
                        # coordonnées aléatoires des loots
                    if event.key == pygame.K_ESCAPE:
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
                        end = False
                        pos_needle.picked = False
                        macgyver.loot[0] = False
                        pos_tube.picked = False
                        macgyver.loot[1] = False
                        pos_ether.picked = False
                        macgyver.loot[2] = False
                        macgyver = Macgyver(520, 40, "m")
                        # coordonnées aléatoires des loots
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    else:
                        pass
        if event.type == pygame.QUIT:
            sys.exit()


    # affichage
    draw_laby()  # affiche le labyrinthe
    windowSurface.blit(img_macgyver, (macgyver.x, macgyver.y))  # affiche MacGyver
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
