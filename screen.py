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
            
            
            clock.tick(60)
            
            screen.fill((255, 255, 255))
            
            pg.display.flip()
            
        pg.quit()