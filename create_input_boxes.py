import pygame as pg

class InputBox:
    def __init__(self, x, y, w, h, text='0', label=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.label = label
        self.font = pg.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, pg.Color('black'))
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    # Return the text when Enter is pressed
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Only allow numbers, decimal points, and minus signs
                    if event.unicode.isdigit() or event.unicode in '.-':
                        self.text += event.unicode
                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, pg.Color('black'))
        return None

    def update(self):
        # Resize the box if the text is too long
        width = max(60, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Draw the input box
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        """Get the numeric value from the input box"""
        try:
            return float(self.text) if self.text else 0.0
        except ValueError:
            return 0.0