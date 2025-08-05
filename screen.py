import pygame as pg

class Screen():
    def __init__(self, size, objects = [], running = True):
        self.size = size
        self.objects = objects
        self.running = running
        
    def add_to_screen(self, object):
        self.objects.append(object)
        
    def create_screen(self):
        return pg.display.set_mode(self.size)
    
    def run(self):
        pg.init()
        
        screen = self.create_screen()
        
        clock = pg.time.Clock()
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            for object in self.objects:
                object.move()
                pg.draw.rect(screen, [255, 0, 0], (object.position[0], object.position[1], object.size[0], object.size[1]))
                pg.display.flip()
                
            clock.tick(60)
            
            screen.fill((255, 255, 255))
            
            pg.display.flip()
            
        pg.quit()