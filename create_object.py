import pygame as pg
from trajectory_formula import trajectory

class Object(pg.sprite.Sprite):
    def __init__(self, name, size, position, screen):
        super().__init__()  # important for Sprite initialization
        
        self.name = name
        self.size = size
        self.screen = screen
        self.speed = [0, 0]
        self.mass = size[0] * size[1]
        self.released = False
        self.dragging = False
        self.dead = False

        # Create the sprite's image & rect
        self.image = pg.Surface(size)
        self.image.fill((255, 0, 0))  # placeholder color
        self.rect = self.image.get_rect()
        self.rect.topleft = position  # starting position

    def move(self):
        # Move using rect so collisions work
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        
        # Remove if off-screen
        if (self.rect.x < 0 or self.rect.x > self.screen.size[0] or self.rect.y > self.screen.size[1]):
            self.dead = True 
        
        if self.speed != [0, 0]:
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
            dx = self.rect.x + self.size[0]/2 - mouse_coords[0]
            dy = (self.rect.y + self.size[1]/2) - mouse_coords[1]

            if self.released:
                self.speed = [dx/8, dy/8]

    def show_trajectory(self, i, dx, dy, dist):
        if dx != 0 and dist != 0:
            pg.draw.circle(
                self.screen.surf, 
                [0, 0, 0], 
                (i + self.rect.x + self.size[0]/2,
                 self.rect.y + self.size[1]/2 + trajectory(i, dx, dy, dist)), 
                2
            )
