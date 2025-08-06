import pygame as pg

class Object():
    def __init__(self, name, size, position, speed, screen):
        self.name = name
        self.size = size
        self.position = position
        self.speed = speed
        self.screen = screen
        self.mass = size[0]*size[1]
    
    def move(self):
        # Check for collisions
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        
        if self.position[0] < 0 or self.position[0] + self.size[0] > self.screen.size[0]:
            if self.position[0] < 0:
                self.position[0] = 0
            else:
                self.position[0] = self.screen.size[0] - self.size[0]
                
            self.speed[0] *= -0.9 # 0.9 instead of 1 to simulate the energy lost on bounce
            
        if self.position[1] < 0 or self.position[1] + self.size[1] > self.screen.size[1]:
            if self.position[1] < 0:
                self.position[1] = 0
            else:
                self.position[1] = self.screen.size[1] - self.size[1]
            
            self.speed[1] *= -0.9 # 0.9 instead of 1 to simulate the energy lost on bounce
            
        self.apply_gravity()
        self.apply_air_resistance()
        
        
        
        
    def apply_gravity(self):
        self.speed[1] += 9.81 / 60
        
    def apply_air_resistance(self):
        if self.speed[0] > 0:
            self.speed[0] -= 0.1/60
        else:
            self.speed[0] += 0.1/60

