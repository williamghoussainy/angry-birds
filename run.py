import pygame as pg
from screen import Screen
from create_object import Object
import pyautogui as ptg
from create_platform import Platform

if __name__ == "__main__":
    screen = Screen()
    
    # Get screen dimensions
    screen_width = ptg.size()[0]
    screen_height = ptg.size()[1]
    
    # Bird launch platform (left side)
    bird_platform = Platform([100, screen_height - 200], screen, True)
    bird = Object("Bird", [30, 30], [135, screen_height - 230], screen)
    
    # === PIG 1 STRUCTURE (Simple elevated platform) ===
    # Base supports
    pig1_support1 = Platform([400, screen_height - 150], screen, False)  # Left vertical support
    pig1_support2 = Platform([500, screen_height - 150], screen, False)  # Right vertical support
    # Main platform
    pig1_platform = Platform([400, screen_height - 200], screen, True)
    pig1 = Object("Pig", [30, 30], [400 + pig1_platform.size[0]/2 - 15, screen_height - 230], screen)
    
    # === PIG 2 STRUCTURE (Tower with multiple levels) ===
    # Ground level supports
    pig2_base1 = Platform([700, screen_height - 150], screen, False)  # Left base
    pig2_base2 = Platform([800, screen_height - 150], screen, False)  # Right base
    # Second level
    pig2_level1 = Platform([700, screen_height - 200], screen, True)
    pig2_support3 = Platform([750, screen_height - 250], screen, False)  # Middle support
    # Top level platform
    pig2_platform = Platform([725, screen_height - 300], screen, True)
    pig2 = Object("Pig", [30, 30], [725 + pig2_platform.size[0]/2 - 15, screen_height - 330], screen)
    
    # === PIG 3 STRUCTURE (Complex castle-like structure) ===
    # Foundation
    pig3_foundation1 = Platform([1000, screen_height - 150], screen, False)
    pig3_foundation2 = Platform([1100, screen_height - 150], screen, False)
    pig3_foundation3 = Platform([1200, screen_height - 150], screen, False)
    # Lower platforms
    pig3_lower1 = Platform([1000, screen_height - 200], screen, True)
    pig3_lower2 = Platform([1150, screen_height - 200], screen, True)
    # Middle supports
    pig3_mid_support1 = Platform([1050, screen_height - 250], screen, False)
    pig3_mid_support2 = Platform([1150, screen_height - 250], screen, False)
    # Top platform
    pig3_platform = Platform([1075, screen_height - 300], screen, True)
    pig3 = Object("Pig", [30, 30], [1075 + pig3_platform.size[0]/2 - 15, screen_height - 330], screen)
    
    # Add all objects to screen
    # Bird and its platform
    screen.add_to_screen(bird)
    screen.add_to_screen(bird_platform)
    
    # Pig 1 structure
    screen.add_to_screen(pig1)
    screen.add_to_screen(pig1_platform)
    screen.add_to_screen(pig1_support1)
    screen.add_to_screen(pig1_support2)
    
    # Pig 2 structure
    screen.add_to_screen(pig2)
    screen.add_to_screen(pig2_platform)
    screen.add_to_screen(pig2_level1)
    screen.add_to_screen(pig2_base1)
    screen.add_to_screen(pig2_base2)
    screen.add_to_screen(pig2_support3)
    
    # Pig 3 structure
    screen.add_to_screen(pig3)
    screen.add_to_screen(pig3_platform)
    screen.add_to_screen(pig3_lower1)
    screen.add_to_screen(pig3_lower2)
    screen.add_to_screen(pig3_foundation1)
    screen.add_to_screen(pig3_foundation2)
    screen.add_to_screen(pig3_foundation3)
    screen.add_to_screen(pig3_mid_support1)
    screen.add_to_screen(pig3_mid_support2)
    
    screen.run()