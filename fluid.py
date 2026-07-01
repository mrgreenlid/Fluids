import pygame
import numpy as np
from typing import List
from algorithms import *


class velocityFunction(Output):
    def __init__(self):
        # Sets up an (initially empty numpy array to store velocities at each point)
        self.__domain = np.empty((self.__line_height, self.__line_length), dtype=np.float32)
        print(__domain)    
    def checkInteract(self):
        return

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable

    def setValue(self, function):
        return




class VectorField(Output):
    class_type = "output"
    __grid_colour =  "#C7C1B8"
    def __init__(self, window : pygame.surface.Surface, rows : int, variable : str, display : bool = False):
        """Creates a vector field to be displayed and store data"""
        self.__window = window
        self.__rows = rows
        self.__variable = variable
        self.__display = display
        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_interval = self.__line_height // self.__rows
    
    def __drawVector(self, tail_x : int, tail_y : int):
        return
    

    def place(self):
        """Draws the vector field"""
        if self.__display:
            # Draws vector field grid and sets up vector arrows
            height = width = self.__grid_line_interval
            for row in range(self.__rows):
                pygame.draw.line(self.__window, self.__grid_colour, (0, height), (self.__line_length, height))
                height += self.__grid_line_interval
                for i in range(2):
                    for j in range(1, self.__rows):
                        if width == 2*self.__rows*self.__grid_line_interval:
                            break

                        self.__drawVector(width, self.__grid_line_interval*j)

                    pygame.draw.line(self.__window, self.__grid_colour, (width, 0), (width, self.__line_height))
                    width += self.__grid_line_interval
                    
    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    def setValue(self, display, rows):
        """Changes variable value"""
        self.__display = display
        self.__rows = rows    
        self.__grid_line_interval = self.__line_height // self.__rows   

        
class Particle(pygame.sprite.Sprite):
    def __init__(self,):
        return 

class Body(pygame.sprite.Sprite):
    def __init__(self,):
        return