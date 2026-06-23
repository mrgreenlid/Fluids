import pygame
import numpy as np
from typing import List
from algorithms import *

class velocityFunction:
    def __init__(self):
        return





class VectorField:
    def __init__(self, window : pygame.surface.Surface, rows : int, key_bind : str, grid_colour : str = "#000000", display : bool = False):
        """Creates"""
        self.__window = window
        self.__grid_colour = grid_colour

        self.__field = np.empty((window.get_height(), window.get_width()), dtype = np.float64)
        self.__rows = rows

        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_start = self.__line_height // self.__rows

        
        self.__key_bind = pygame.key.key_code(key_bind)
        self.__display = display

    def update(self, rows : int = None):
        self.__rows = rows

        self.__grid_line_start = self.__line_height // self.__rows

    def place(self):
        if self.__display:
            spacing = height = width = self.__grid_line_start
            for row in range(self.__rows):
                pygame.draw.line(self.__window, self.__grid_colour, (0, height), (self.__line_length, height))
                height += spacing
                pygame.draw.line(self.__window, self.__grid_colour, (width, 0), (width, self.__line_height ))
                width += spacing
                pygame.draw.line(self.__window, self.__grid_colour, (width , 0), (width, self.__line_height ))
                width += spacing

    def checkInteract(self, event : pygame.event.Event, keys : List[bool]):
        if self.__key_bind:
            if typing(event):
                if keys[self.__key_bind]:
                    self.__display = toggleVariable(self.__display)
            

        
class Particle(pygame.sprite.Sprite):
    def __init__(self,):

        return 

class Body(pygame.sprite.Sprite):
    def __init__(self,):
        return