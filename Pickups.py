import random
import pygame

class Pickup(object):
    def __init__(self):
        self.Health = pygame.image.load("Sprites\\Heart_2.png")
        self.Pistol = pygame.image.load("Sprites\\UIBullet.png")
        self.Shotgun = pygame.image.load("Sprites\\UIShell.png")
        self.minigun = pygame.image.load("Sprites\\MiniGun.png")
        self.Minigun = pygame.image.load("Sprites\\UIMini.png")
        self.Key = pygame.image.load("Sprites\\Key.png")
        self.items = ["HP"]
        self.dropped_list = []
        self.width = 128
        self.height = 128

    def drop(self, x, y):
        item = random.choice(self.items)
        self.dropped_list.append([item, x, y, self.width, self.height])

    def render(self, ds):
        for item in self.dropped_list:
            if item[0] == "HP":
                ds.blit(self.Health, (item[1], item[2]))
            if item[0] == "pAmmo":
                ds.blit(self.Pistol, (item[1], item[2]))
            if item[0] == "sAmmo":
                ds.blit(self.Shotgun, (item[1], item[2]))
            if item[0] == "mAmmo":
                ds.blit(self.Minigun, (item[1], item[2]))
            if item[0] == "miniGun":
                ds.blit(self.minigun, (item[1], item[2]))
            if item[0] == "key":
                ds.blit(self.Key, (item[1], item[2]))

