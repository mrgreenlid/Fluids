import pygame
import numpy as np
import sqlite3 as sqlite
from typing import List, Tuple
from algorithms import *

# Creates table in fluids database to store velocity functions
with sqlite.Connection("fluids.db") as conn:
    conn.cursor().execute("""CREATE TABLE IF NOT EXISTS function (
                written TEXT PRIMARY KEY UNIQUE,
                exponential INTEGER,
                magnitude TEXT,
                argument TEXT)
                """)
    conn.commit()

class VectorField(Output):
    __grid_colour =  "#C7C1B8"
    def __init__(self, window : pygame.surface.Surface, rows : int, variable : List[str] , display : bool = False):
        """Creates a vector field to be displayed and store data"""
        self.__window = window
        self.__rows = rows
        self.__variable = variable
        self.__display = display
        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_interval = self.__line_height // self.__rows
    
        self.__plane = np.empty((self.__line_height, self.__line_length), dtype=np.float64)
        self.__flow = False

        self.__velocity_function = ()

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

    def __map(self):
        ...

    def setVelocityFunction(self, velocity_function : Tuple[str] | Tuple[int]):
        if self.__velocity_function != velocity_function:
            self.__velocity_function = velocity_function
            self.__map()

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    def setValue(self, display, rows, flow):
        """Changes variable value"""
        self.__display = display
        self.__rows = rows   
        self.__flow = flow
        self.__grid_line_interval = self.__line_height // self.__rows   
    

class Particle(pygame.sprite.Sprite):
    def __init__(self,):
        return 

class Body(pygame.sprite.Sprite):
    def __init__(self,):
        return