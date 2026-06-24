import pygame
import numpy as np
from typing import List
from algorithms import *

class velocityFunction:
    def __init__(self):
        return




class VectorField:
    __grid_colour =  "#C7C1B8"
    def __init__(self, window : pygame.surface.Surface, rows : int, key_bind : str, display : bool = False):
        """Creates a vector field to be displayed and store data"""
        self.__window = window
        self.__rows = rows

        

        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_start = self.__line_height // self.__rows



        self.__key_bind = pygame.key.key_code(key_bind)
        self.__display = display



    def __drawVector(self, tail_x : int, tail_y : int):
        return
        
    def place(self):
        """Draws the vector field"""
        if self.__display:
            height = width = self.__grid_line_start
            for row in range(self.__rows):
                pygame.draw.line(self.__window, self.__grid_colour, (0, height), (self.__line_length, height))
<<<<<<< HEAD
                height += self.__grid_line_interval
                for i in range(2):
                    for j in range(1, self.__rows):
                        self.__drawVector(width, self.__grid_line_interval*j)
                    pygame.draw.line(self.__window, self.__grid_colour, (width, 0), (width, self.__line_height ))
                    width += self.__grid_line_interval
                    
=======
                height += self.__grid_line_start
                pygame.draw.line(self.__window, self.__grid_colour, (width, 0), (width, self.__line_height ))
                width += self.__grid_line_start
                pygame.draw.line(self.__window, self.__grid_colour, (width , 0), (width, self.__line_height ))
                width += self.__grid_line_start
>>>>>>> parent of 04ad0f5 (Optimising after concideration of vector field)

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