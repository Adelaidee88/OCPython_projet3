import pygame

class Sprite :

    def __init__(self):
        self.img_mur = pygame.image.load("resources/wall.png")
        self.img_sol = pygame.image.load("resources/ground.png")
        self.img_murd = pygame.image.load("resources/murd.png")
        self.img_macgyver = pygame.image.load("resources/macg.png")
        self.img_needle = pygame.image.load("resources/needle.png")
        self.inv_needle = pygame.image.load("resources/needle_loot.png")
        self.img_tube = pygame.image.load("resources/tube.png")
        self.inv_tube = pygame.image.load("resources/tube_loot.png")
        self.img_ether = pygame.image.load("resources/ether.png")
        self.inv_ether = pygame.image.load("resources/ether_loot.png")
        self.screen_win = pygame.image.load("resources/screen_win.png")
        self.screen_lose = pygame.image.load("resources/screen_lose.png")

if __name__ == "__main__":
    pass