import pygame as pg
from screen import Screen
from create_object import Object

if __name__ == "__main__":
    screen = Screen([800, 600])
    
    obj1 = Object("Pig", [60, 30], [500, 100], [2, 6], screen)
    obj2 = Object("Pig", [60, 30], [300, 100], [5, 4], screen)
    
    screen.add_to_screen(obj1)
    screen.add_to_screen(obj2)
    
    screen.run()