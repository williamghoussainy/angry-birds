import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, position, screen, horizontalplatform):
        super().__init__()
        
        self.name = "Platform"
        if horizontalplatform:
            self.size = [100, 50]
        else:
            self.size = [50, 100]
        self.screen = screen
        self.mass = self.size[0] * self.size[1]
        self.speed = [0, 0]
        
        # Create image + rect
        self.image = pg.Surface(self.size)
        self.image.fill((100, 100, 100))  # grey platform
        self.rect = self.image.get_rect()
        self.rect.topleft = position
