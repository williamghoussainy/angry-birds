import pygame as pg
import time as t
import pyautogui as ptg
from create_object import Object


class Screen():
    def __init__(self, size = list(ptg.size())):
        self.size = size
        self.objects = []
        self.running = True
        self.surf = pg.Surface(self.size)
        if self.size == list(ptg.size()):
            self.screen = pg.display.set_mode(self.size, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(self.size)
        self.dragging_object_index = -1
        
    def add_to_screen(self, object):
        self.objects.append(object)
    
    def check_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                recti = self.objects[i].rect
                rectj = self.objects[j].rect
                
                if recti.colliderect(rectj):
                    overlap_x = min(recti.right, rectj.right) - max(recti.left, rectj.left)
                    overlap_y = min(recti.bottom, rectj.bottom) - max(recti.top, rectj.top) 
                    
                    if overlap_x < overlap_y:
                        # Horizontal collision
                        if recti.right < rectj.right:
                            if self.objects[i].name != "Platform":
                                self.objects[i].rect.x = self.objects[j].rect.x - self.objects[i].size[0]
                            if self.objects[j].name != "Platform":
                                self.objects[j].rect.x = self.objects[i].rect.x + self.objects[i].size[0]

                        else:
                            if self.objects[j].name != "Platform":
                                self.objects[j].rect.x = self.objects[i].rect.x - self.objects[j].size[0]
                            if self.objects[i].name != "Platform":
                                self.objects[i].rect.x = self.objects[j].rect.x + self.objects[j].size[0]
                        
                        # Apply collision physics for horizontal collision
                        initialSpeedi = self.objects[i].speed[0]
                        initialSpeedj = self.objects[j].speed[0]
                        self.objects[i].speed[0] = (2*self.objects[j].mass*initialSpeedj + (self.objects[i].mass - self.objects[j].mass)*initialSpeedi) / (self.objects[i].mass + self.objects[j].mass)
                        self.objects[j].speed[0] = (2*self.objects[i].mass*initialSpeedi + (self.objects[j].mass - self.objects[i].mass)*initialSpeedj) / (self.objects[i].mass + self.objects[j].mass)
                    else:
                        # Vertical collision
                        if recti.bottom < rectj.bottom:
                            if self.objects[i].name != "Platform":
                                self.objects[i].rect.y = self.objects[j].rect.y - self.objects[i].size[1]
                            if self.objects[j].name != "Platform":
                                self.objects[j].rect.y = self.objects[i].rect.y + self.objects[i].size[1]
                        else:
                            if self.objects[j].name != "Platform":
                                self.objects[j].rect.y = self.objects[i].rect.y - self.objects[j].size[1]
                            if self.objects[i].name != "Platform":
                                self.objects[i].rect.y = self.objects[j].rect.y + self.objects[j].size[1]

                        # Apply collision physics for vertical collision
                        initialSpeedi = self.objects[i].speed[1]
                        initialSpeedj = self.objects[j].speed[1]
                        
                        # Check if either object is a platform for damping
                        damping_factor = 1.0
                        if self.objects[i].name == "Platform" or self.objects[j].name == "Platform":
                            damping_factor = 0.5
                        
                        new_speed_i = (2*self.objects[j].mass*initialSpeedj + (self.objects[i].mass - self.objects[j].mass)*initialSpeedi) / (self.objects[i].mass + self.objects[j].mass)
                        new_speed_j = (2*self.objects[i].mass*initialSpeedi + (self.objects[j].mass - self.objects[i].mass)*initialSpeedj) / (self.objects[i].mass + self.objects[j].mass)
                        
                        self.objects[i].speed[1] = new_speed_i * damping_factor
                        self.objects[j].speed[1] = new_speed_j * damping_factor
                        
                        # Stop jittering by setting very small speeds to zero
                        velocity_threshold = 0.5
                        if abs(self.objects[i].speed[1]) < velocity_threshold:
                            self.objects[i].speed[1] = 0
                        if abs(self.objects[j].speed[1]) < velocity_threshold:
                            self.objects[j].speed[1] = 0
                            
                        # Additional check: if object is resting on platform, stop all movement
                        if self.objects[i].name == "Platform" and abs(self.objects[j].speed[1]) < 1.0:
                            self.objects[j].speed[1] = 0
                        elif self.objects[j].name == "Platform" and abs(self.objects[i].speed[1]) < 1.0:
                            self.objects[i].speed[1] = 0


    def run(self):
        pg.init()
            
        
        self.surf.fill((0, 100, 255))
        
        clock = pg.time.Clock()
        
        dragging = False
        
        while self.running:
            mouse_coords = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    for object in self.objects:
                        if object.name != "Platform":
                            if (object.rect.x <= mouse_coords[0] <= object.rect.x + object.size[0]) and (object.rect.y <= mouse_coords[1] <= object.rect.y + object.size[1]) and not object.released:
                                object.dragging = True
                                self.dragging_object_index = self.objects.index(object)
                                dragging = True
                if event.type == pg.MOUSEBUTTONUP:
                    if self.dragging_object_index != -1:
                        object = self.objects[self.dragging_object_index]
                        if object.name != "Platform":
                            object.dragging = False
                            object.released = True
                            object.drag(mouse_coords)
                    dragging = False
                
                if dragging:
                    if self.dragging_object_index != -1:
                        object = self.objects[self.dragging_object_index]
                        if object.name != "Platform":
                            object.drag(mouse_coords) 
                                        
            self.check_collisions()
            
            for object in self.objects:
                if object.name == "Platform":
                    pg.draw.rect(self.surf, [225, 198, 153], (object.rect.x, object.rect.y, object.size[0], object.size[1]))

                else:
                    object.move()
                    
                    # Draw trajectory for dragging objects
                    if object.dragging:
                        mouse_coords = pg.mouse.get_pos()
                        dx = object.rect.x + object.size[0]/2 - mouse_coords[0]
                        dy = (object.rect.y + object.size[1]/2) - mouse_coords[1]
                        dist = ((dx)**2 + (dy)**2) ** 0.5
                        
                        for i in range(0, 900, 30):
                            object.show_trajectory(i, dx, dy, dist)
                    
                    if object.name == "Bird":
                        pg.draw.rect(self.surf, [200, 0, 0], (object.rect.x, object.rect.y, object.size[0], object.size[1]))
                        print(object.speed)
                    elif object.name == "Pig":
                        pg.draw.rect(self.surf, [0, 150, 0], (object.rect.x, object.rect.y, object.size[0], object.size[1]))
                    
            if self.dragging_object_index != -1:
                object = self.objects[self.dragging_object_index]
                if object.dead or (object.speed == [0, 0] and object.released):
                    self.objects[self.dragging_object_index] = Object("Bird", [30, 30], [135, ptg.size()[1] - 230], self)
                    self.dragging_object_index = -1
                
            clock.tick(60)
            
            self.screen.fill((0, 255, 255))
            
            self.screen.blit(self.surf, (0, 0))
            
            pg.display.flip()
            
            self.surf.fill((0, 100, 255))
            
        pg.quit()