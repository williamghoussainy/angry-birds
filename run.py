import pygame as pg
from screen import Screen
from create_object import Object
import pyautogui as ptg

if __name__ == "__main__":
    # screen = Screen()
    screen = Screen([800, 600], False)
    
    # obj1 = Object("Bird", [30, 30], [200, ptg.size()[1] - 200], screen)
    obj1 = Object("Bird", [30, 30], [200, 100], screen)
    obj2 = Object("Pig", [30, 30], [500, 300], screen)
    
    screen.add_to_screen(obj1)
    screen.add_to_screen(obj2)
    
    screen.run()