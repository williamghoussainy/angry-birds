import pygame as pg
import time as t
import pyautogui as ptg
from create_object import Object
from create_input_boxes import InputBox


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
        
        # Initialize font for text rendering
        pg.font.init()
        self.font = pg.font.Font(None, 36)
        
        # Create input boxes for quadratic coefficients
        self.setup_input_boxes()
        
    def setup_input_boxes(self):
        """Setup input boxes for quadratic trajectory coefficients"""
        # Positioning the input boxes at the top of the screen
        start_x = 50
        start_y = 30
        box_width = 60
        box_height = 30
        spacing = 150
        
        # Create input boxes for a, b, c coefficients
        self.input_box_a = InputBox(start_x, start_y, box_width, box_height, text='0.01', label='a')
        self.input_box_b = InputBox(start_x + spacing, start_y, box_width, box_height, text='3', label='b') 
        self.input_box_c = InputBox(start_x + spacing*2, start_y, box_width, box_height, text='0', label='c')
        
        self.input_boxes = [self.input_box_a, self.input_box_b, self.input_box_c]
    
    def draw_trajectory_equation(self):
        """Draw the trajectory equation with current coefficient values"""
        # Get coefficient values
        a = self.input_box_a.get_value()
        b = self.input_box_b.get_value() 
        c = self.input_box_c.get_value()
        
        # Format the equation text
        if a != 0:
            equation_text = f"-({a})x² + ({b})x + ({c})"

            # Render and draw the equation
            text_surface = self.font.render(equation_text, True, (255, 255, 255))
            self.surf.blit(text_surface, (50, 80))
        
        # Draw labels for input boxes
        label_font = pg.font.Font(None, 24)
        
        # Label for 'a' coefficient
        a_label = label_font.render("a:", True, (255, 255, 255))
        self.surf.blit(a_label, (50, 10))
        
        # Label for 'b' coefficient  
        b_label = label_font.render("b:", True, (255, 255, 255))
        self.surf.blit(b_label, (200, 10))
        
        # Label for 'c' coefficient
        c_label = label_font.render("c:", True, (255, 255, 255))
        self.surf.blit(c_label, (350, 10))
        
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

        show_trajectory = True
        

        while self.running:
            a = self.input_box_a.get_value()
            b = self.input_box_b.get_value() 
            c = self.input_box_c.get_value()
            
            mouse_coords = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                    
                # Handle input box events
                for input_box in self.input_boxes:
                    result = input_box.handle_event(event)
                    if result is not None:
                        print(f"Updated coefficient: {result}")
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (ptg.size()[0] - 100 <= mouse_coords[0] <= ptg.size()[0]) and (0 <= mouse_coords[1] <= 50):
                        for object in self.objects:
                            if object.name == "Bird":
                                object.shoot(a, b, c)
            
                                
            self.check_collisions()
            
            shoot_button = pg.Rect(ptg.size()[0] - 100, 0, 100, 50)

            pg.draw.rect(self.surf, (255, 0, 0), shoot_button)
            
            # Update input boxes
            for input_box in self.input_boxes:
                input_box.update()
            
            for object in self.objects:
                if object.name == "Platform":
                    pg.draw.rect(self.surf, [225, 198, 153], (object.rect.x, object.rect.y, object.size[0], object.size[1]))

                else:
                    object.move()
                    
                    if show_trajectory and object.name == "Bird":                   
                        for i in range(0, 900, 30):
                            object.show_trajectory(i, a, b, c)
                    
                    if object.name == "Bird":
                        pg.draw.rect(self.surf, [200, 0, 0], (object.rect.x, object.rect.y, object.size[0], object.size[1]))
                        if object.dead or object.speed == [0, 0] and object.released:
                            self.objects[self.objects.index(object)] = Object("Bird", [30, 30], [135, pg.display.get_surface().get_height() - 230], self)
                    elif object.name == "Pig":
                        pg.draw.rect(self.surf, [0, 150, 0], (object.rect.x, object.rect.y, object.size[0], object.size[1]))
                    

            for input_box in self.input_boxes:
                input_box.draw(self.surf)

            self.draw_trajectory_equation()

            clock.tick(60)
            
            self.screen.fill((0, 255, 255))
            
            self.screen.blit(self.surf, (0, 0))
            
            pg.display.flip()
            
            self.surf.fill((0, 100, 255))
            
        pg.quit()