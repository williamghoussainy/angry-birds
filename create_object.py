import pygame as pg
from trajectory_formula import trajectory

class Object():
    def __init__(self, name, size, position, screen):
        self.name = name
        self.size = size
        self.position = position
        self.screen = screen
        self.speed = [0, 0]
        self.mass = size[0]*size[1]
        self.released = False
        self.dragging = False
    
    def move(self):
        # Check for collisions
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        
        if self.position[0] < 0 or self.position[0] > self.screen.size[0] or self.position[1] > self.screen.size[1]:
            self.screen.objects.remove(self)
        
        if self.released:    
            self.apply_gravity()
            self.apply_air_resistance()
        
    def apply_gravity(self):
        self.speed[1] += 9.81 / 60
        
    def apply_air_resistance(self):
        if self.speed[0] > 0:
            self.speed[0] -= 0.1/60
        else:
            self.speed[0] += 0.1/60
    
    def drag(self, mouse_coords):
        if self.name != "Pig":
            dx = self.position[0] + self.size[0]/2 - mouse_coords[0]
            dy = (self.position[1] + self.size[1]/2) - mouse_coords[1]

                    
            if self.released:
                self.speed = [dx/8, dy/8]

    def show_trajectory(self, i, dx, dy, dist):
        if dx != 0 and dist != 0:
            pg.draw.circle(self.screen.surf, [0, 0, 0], (i + self.position[0] + self.size[0]/2, self.position[1] + self.size[1]/2 + trajectory(i, dx, dy, dist)), 2)
