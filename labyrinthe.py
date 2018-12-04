import pygame, sys
from parse import parse
from square import Square
from macgyver import Macgyver
from loot import Loot
import random
from murdock import Murdock
from sprite import Sprite


laby = open("maze.txt", "r")  # open file maze.txt
content = laby.read()  # return file content

maze = []  # create empty final list for the labyrinth
maze_list = []  # create empty list of lines list
maze_str = content.splitlines()  # separate each line of file as string


for line in maze_str:
    maze_list.append(parse(line))  # parse function to fill the list

for line in maze_list:
    maze.append(parse(line))  # parse function to fill the final list


pygame.init()

windowSurface = pygame.display.set_mode((600, 600), 0, 32)  # window of 600x600 px
pygame.display.set_caption('Labyrinth')  # named Labyrinth
pygame.mixer.music.load("resources/bonk.wav")  # collision sound loaded


class Labyrinth:

    def __init__(self):
        self.sprite = Sprite()
        self.macgyver = Macgyver(40, 520, "m")  # create Macgyver object
        self.murdock = Murdock(520, 560, "murdock")  # create Murdock object
        self.win = False
        self.end = False
        self.objects = random.sample(self.way(), 3)  # take 3 random positions in the list created by the way function
        self.needle = self.objects[0]  # the needle correspond to the first object of the random list
        self.tube = self.objects[1]  # the tube correspond to the second object of the random list
        self.ether = self.objects[2]  # the ether correspond to the third object of the random list
        self.pos_needle = Loot(self.needle.x * 40, self.needle.y * 40,
                               "needle")  # create needle as a Loot object
        self.pos_tube = Loot(self.tube.x * 40, self.tube.y * 40, "tube")  # create tube as a Loot object
        self.pos_ether = Loot(self.ether.x * 40, self.ether.y * 40, "ether")  # create ether as a Loot object

    def randomize_object(self):
        self.objects = random.sample(self.way(), 3)  # take 3 random positions in the list created by the way function
        self.needle = self.objects[0]  # the needle correspond to the first object of the random list
        self.tube = self.objects[1]  # the tube correspond to the second object of the random list
        self.ether = self.objects[2]  # the ether correspond to the third object of the random list
        self.pos_needle = Loot(self.needle.x * 40, self.needle.y * 40, "needle")  # create needle as a Loot object
        self.pos_tube = Loot(self.tube.x * 40, self.tube.y * 40, "tube")  # create tube as a Loot object
        self.pos_ether = Loot(self.ether.x * 40, self.ether.y * 40, "ether")  # create ether as a Loot object

    def reinit(self):
        self.macgyver = Macgyver(40, 520, "m")  # create Macgyver object
        self.murdock = Murdock(520, 560, "murdock")  # create Murdock object
        self.win = False
        self.end = False

    def draw_laby(self, sprite):
        """Draws the labyrinth from the maze list created from maze.txt"""
        i = 0
        while i < 600:  # cases texture from name value of maze
            j = 0
            while j < 600:
                case = Square(i // 40, j // 40, maze[i // 40][j // 40])
                value_case = case.name

                if value_case == "x":
                    windowSurface.blit(sprite.img_mur, (case.x*40, case.y*40))
                elif value_case == " ":
                    windowSurface.blit(sprite.img_sol, (case.x * 40, case.y * 40))
                elif value_case == "m":
                    windowSurface.blit(sprite.img_sol, (case.x * 40, case.y * 40))
                else:
                    windowSurface.blit(sprite.img_murd, (self.murdock.x, self.murdock.y))
                j = j + 40
            i = i + 40

    def way(self):
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

    def mac_move(self, event):
        if event.key == pygame.K_LEFT:  # if left arrow
            if maze[self.macgyver.x // 40 - 1][self.macgyver.y // 40] == " " or maze[self.macgyver.x // 40][self.macgyver.y // 40 + 1] == "m":
                self.macgyver.x = self.macgyver.x - 40  # move left
            else:
                pygame.mixer.music.play()
        elif event.key == pygame.K_UP:  # if up arrow
            if maze[self.macgyver.x // 40][self.macgyver.y // 40 - 1] == " ":
                self.macgyver.y = self.macgyver.y - 40  # move up
            else:
                pygame.mixer.music.play()
        elif event.key == pygame.K_RIGHT:  # if right arrow
            if maze[self.macgyver.x // 40 + 1][self.macgyver.y // 40] == " ":
                self.macgyver.x = self.macgyver.x + 40  # move right
            else:
                pygame.mixer.music.play()
        elif event.key == pygame.K_DOWN:  # if down arrow
            if maze[self.macgyver.x // 40][self.macgyver.y // 40 + 1] == " " or maze[self.macgyver.x // 40][self.macgyver.y // 40 + 1] == "v":
                self.macgyver.y = self.macgyver.y + 40  # move down
            else:
                pygame.mixer.music.play()  # play collision sound

    def get_item(self):
        if self.macgyver.x == self.pos_needle.x and self.macgyver.y == self.pos_needle.y:  # if MacGyver reaches needle
            self.pos_needle.picked = True
            self.macgyver.loot[0] = True
        if self.macgyver.x == self.pos_tube.x and self.macgyver.y == self.pos_tube.y:  # if MacGyver reaches tube
            self.pos_tube.picked = True
            self.macgyver.loot[1] = True
        if self.macgyver.x == self.pos_ether.x and self.macgyver.y == self.pos_ether.y:  # if MacGyver reaches ether
            self.pos_ether.picked = True
            self.macgyver.loot[2] = True

    def end_game(self, event):
        if self.macgyver.x == self.murdock.x and self.macgyver.y == self.murdock.y:  # if MacGyver reaches Murdock
            self.end = True
            if self.macgyver.loot[0] and self.macgyver.loot[1] and self.macgyver.loot[2]:
                self.win = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # replay the game, reload initial conditions
                        self.randomize_object()
                        self.reinit()
                    if event.key == pygame.K_ESCAPE:  # close the game
                        sys.exit()
            else:
                self.win = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # replay the game, reload initial conditions
                        self.randomize_object()
                        self.reinit()
                    if event.key == pygame.K_ESCAPE:  # close the game
                        sys.exit()
        if event.type == pygame.QUIT:
            sys.exit()

    def game_loop(self):

        self.reinit()
        self.randomize_object()

        while 1:
            for event in pygame.event.get():
                # move
                if self.end == False:
                    if event.type == pygame.KEYDOWN :
                        self.mac_move(event)
                        self.get_item()

                self.end_game(event)
            self.display()

    def display(self):
        self.draw_laby(self.sprite)  # display labyrinth
        windowSurface.blit(self.sprite.img_macgyver, (self.macgyver.x, self.macgyver.y))  # display MacGyver
        if self.pos_needle.picked == False:
            windowSurface.blit(self.sprite.img_needle, (self.pos_needle.x, self.pos_needle.y))  # display needle on the labyrinth
        else:
            windowSurface.blit(self.sprite.inv_needle, (0, 0))  # display needle in the inventory
        if self.pos_tube.picked == False:
            windowSurface.blit(self.sprite.img_tube, (self.pos_tube.x, self.pos_tube.y))  # display tube on the labyrinth
        else:
            windowSurface.blit(self.sprite.inv_tube, (0, 40))  # display tube in the inventory
        if self.pos_ether.picked == False:
            windowSurface.blit(self.sprite.img_ether, (self.pos_ether.x, self.pos_ether.y))  # display ether in the labyrinth
        else:
            windowSurface.blit(self.sprite.inv_ether, (0, 80))  # display ether in the inventory
        if self.end and self.win:
            windowSurface.blit(self.sprite.screen_win, (0, 0))  # display victory screen
        if self.end and self.win == False:
            windowSurface.blit(self.sprite.screen_lose, (0, 0))  # display defeat screen
        pygame.display.update()

if __name__ == "__main__":
    labyrinth = Labyrinth()
    labyrinth.game_loop()
