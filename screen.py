import pygame as pg
import time as t
import mouse

class Screen():
    def __init__(self, size):
        self.size = size
        self.objects = []
        self.running = True
        self.surf = pg.Surface(self.size)
        self.screen = pg.display.set_mode(self.size)
        
    def add_to_screen(self, object):
        self.objects.append(object)
    
    def check_collisions(self):
        for i in range(len(self.objects)):
                for j in range(i + 1, len(self.objects)):
                    recti = pg.Rect(self.objects[i].position[0], self.objects[i].position[1], self.objects[i].size[0], self.objects[i].size[1])
                    rectj = pg.Rect(self.objects[j].position[0], self.objects[j].position[1], self.objects[j].size[0], self.objects[j].size[1])
                    
                    if recti.colliderect(rectj):
                        overlap_x = min(recti.right, rectj.right) - max(recti.left, rectj.left)
                        overlap_y = min(recti.bottom, rectj.bottom) - max(recti.top, rectj.top) 
                        
                        if overlap_x < overlap_y:
                            if recti.right < rectj.right:
                                self.objects[i].position[0] = self.objects[j].position[0] - self.objects[i].size[0] - 1
                                
                                
                            else:
                                self.objects[j].position[0] = self.objects[i].position[0] - self.objects[j].size[0] - 1
                            
                            initialSpeedi = self.objects[i].speed[0]
                            initialSpeedj = self.objects[j].speed[0]
                            self.objects[i].speed[0] = (2*self.objects[j].mass*initialSpeedj + (self.objects[i].mass - self.objects[j].mass)*initialSpeedi) / (self.objects[i].mass + self.objects[j].mass)
                            self.objects[j].speed[0] = (2*self.objects[i].mass*initialSpeedi + (self.objects[j].mass - self.objects[i].mass)*initialSpeedj) / (self.objects[i].mass + self.objects[j].mass)
                                
                                 
                            
                        else:
                            if recti.bottom < rectj.bottom:
                                self.objects[i].position[1] = self.objects[j].position[1] - self.objects[i].size[1] - 1
                                
                            else:
                                self.objects[j].position[1] = self.objects[i].position[1] - self.objects[j].size[1] - 1

                            initialSpeedi = self.objects[i].speed[1]
                            initialSpeedj = self.objects[j].speed[1]
                            self.objects[i].speed[1] = (2*self.objects[j].mass*initialSpeedj + (self.objects[i].mass - self.objects[j].mass)*initialSpeedi) / (self.objects[i].mass + self.objects[j].mass)
                            self.objects[j].speed[1] = (2*self.objects[i].mass*initialSpeedi + (self.objects[j].mass - self.objects[i].mass)*initialSpeedj) / (self.objects[i].mass + self.objects[j].mass)
    
    def run(self):
        pg.init()
        
        self.surf.fill((255, 255, 255))
        
        clock = pg.time.Clock()
        
        dragging = False
        
        while self.running:
            mousex, mousey = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for object in self.objects:
                        if (object.position[0] <= mousex <= object.position[0] + object.size[0]) and (object.position[1] <= mousey <= object.position[1] + object.size[1]) and not object.dragged:
                            object.dragging = True
                            dragging = True
                elif event.type == pg.MOUSEBUTTONUP:
                    for object in self.objects:
                        if object.dragging:
                            object.dragging = False
                            object.dragged = True
                            object.drag(mouse_coords)
                    dragging = False
                
                if dragging:
                    mouse_coords = pg.mouse.get_pos()
                    for object in self.objects:
                        if object.dragging:
                            object.drag(mouse_coords) 
                    
                                        
            for object in self.objects:
                object.move()
                pg.draw.rect(self.surf, [255, 0, 0], (object.position[0], object.position[1], object.size[0], object.size[1]))
                pg.display.flip()
            
            
            self.check_collisions()
            
            clock.tick(60)
            
            self.screen.fill((255, 255, 255))
            
            self.screen.blit(self.surf, (0, 0))
            
            self.surf.fill((255, 255, 255))
            
            pg.display.flip()
            
        pg.quit()