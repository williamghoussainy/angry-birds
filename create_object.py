import pygame as pg

class Object():
    def __init__(self, name, size, position, speed, screen):
        self.name = name
        self.size = size
        self.position = position
        self.speed = speed
        self.screen = screen
    
    
    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

