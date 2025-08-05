import pygame as pg
from screen import Screen
from create_object import Object

if __name__ == "__main__":
    screen = Screen([600, 600])
    
    obj1 = Object("Pig", [10, 10], [40, 40], [4, 4], screen)
    
    screen.add_to_screen(obj1)
    
    screen.run()