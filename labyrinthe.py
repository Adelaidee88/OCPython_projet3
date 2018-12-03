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

maze = []  # create empty final list for the labyrinth
maze_list = []  # create empty list of lines list
maze_str = contenu.splitlines()  # separate each line of file as string


for line in maze_str:
    maze_list.append(parse(line))  # parse function to fill the list

for line in maze_list:
    maze.append(parse(line))  # parse function to fill the final list


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


macgyver = Macgyver(520, 40, "m")  # create Macgyver object
murdock = Murdock(520, 560, "murdock") # create Murdock object

objects = random.sample(way(), 3)  # take 3 random positions in the list created by the way function

needle = objects[0]  # the needle correspond to the first object of the random list
pos_needle = Loot(needle.x*40, needle.y*40, "needle")  # create needle as a Loot object

tube = objects[1]  # the tube correspond to the second object of the random list
pos_tube = Loot(tube.x*40, tube.y*40, "tube")  # crete tube as a Loot object

ether = objects[2]  # the ethere correspond to the third object of the random list
pos_ether = Loot(ether.x*40, ether.y*40, "ether")  # create ether as a Loot object

win = False
lose = False
end = False

while 1:
    for event in pygame.event.get():

        # move
        if end == False:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:  # if left arrow
                    if maze[macgyver.x//40 - 1][macgyver.y//40] == " ":
                        macgyver.x = macgyver.x - 40  # move left
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_UP:  # if up arrow
                    if maze[macgyver.x//40][macgyver.y//40 - 1] == " ":
                        macgyver.y = macgyver.y - 40  # move up
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_RIGHT:  # if right arrow
                    if maze[macgyver.x//40 + 1][macgyver.y//40] == " ":
                        macgyver.x = macgyver.x + 40  # move right
                    else:
                        pygame.mixer.music.play()
                elif event.key == pygame.K_DOWN:  # if down arrow
                    if maze[macgyver.x//40][macgyver.y//40 + 1] == " " or maze[macgyver.x//40][macgyver.y//40 + 1] == "v":
                        macgyver.y = macgyver.y + 40  # move down
                    else:
                        pygame.mixer.music.play()  # play collision sound
                else:
                    pass

            # loot
            if macgyver.x == pos_needle.x and macgyver.y == pos_needle.y:  # if MacGyver reaches needle
                pos_needle.picked = True
                macgyver.loot[0] = True
            if macgyver.x == pos_tube.x and macgyver.y == pos_tube.y:  # if MacGyver reaches tube
                pos_tube.picked = True
                macgyver.loot[1] = True
            if macgyver.x == pos_ether.x and macgyver.y == pos_ether.y:  # if MacGyver reaches ether
                pos_ether.picked = True
                macgyver.loot[2] = True

        # endgame
        if macgyver.x == murdock.x and macgyver.y == murdock.y:  # if MacGyver reaches Murdock
            end = True
            if macgyver.loot[0] and macgyver.loot[1] and macgyver.loot[2]:
                win = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # replay the game
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
                    if event.key == pygame.K_ESCAPE:  # close the game
                        sys.exit()
                    else:
                        pass
            else:
                lose = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # replay the game
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
                    if event.key == pygame.K_ESCAPE:  # close the game
                        sys.exit()
                    else:
                        pass
        if event.type == pygame.QUIT:
            sys.exit()


    # display
    draw_laby()  # display labyrinth
    windowSurface.blit(img_macgyver, (macgyver.x, macgyver.y))  # display MacGyver
    if pos_needle.picked == False:
        windowSurface.blit(img_needle, (pos_needle.x, pos_needle.y))  # display needle on the labyrinth
    else:
        windowSurface.blit(inv_needle, (0, 0))  # display needle in the inventory
    if pos_tube.picked == False:
        windowSurface.blit(img_tube, (pos_tube.x, pos_tube.y))  # display tube on the labyrinth
    else:
        windowSurface.blit(inv_tube, (0, 40))  # display tube in the inventory
    if pos_ether.picked == False:
        windowSurface.blit(img_ether, (pos_ether.x, pos_ether.y))  # display ether in the labyrinth
    else:
        windowSurface.blit(inv_ether, (0, 80))  # display ether in the inventory
    if win == True:
        windowSurface.blit(screen_win, (0, 0))  # display victory screen
    if lose == True:
        windowSurface.blit(screen_lose, (0, 0))  # display defeat screen
    pygame.display.update()
