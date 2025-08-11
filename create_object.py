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

    def apply_gravity(self):
        self.speed[1] += (9.81 * 100) / (60**2)  # pixels/frame²
        
    
    def shoot(self, a, b, c):
        if self.name != "Pig" and a > 0 and not self.released:
            self.rect.y -= c
            
            g_per_frame = (9.81 * 100) / (60**2)  # pixels/frame²

            
            vx = ((g_per_frame) / (2 * a)) ** 0.5
            vy = - b * vx
            self.speed = [vx, vy]
            self.released = True



    def show_trajectory(self, i, a, b, c):
        if a > 0 and not self.released:
            pg.draw.circle(
                self.screen.surf, 
                [0, 0, 0], 
                (i + self.rect.x + self.size[0]/2,
                 self.rect.y + self.size[1]/2 + trajectory(i, a, b, c)),
                2
            )
