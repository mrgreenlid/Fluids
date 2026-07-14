import pygame
import numpy as np
import sqlite3 as sqlite
from typing import List, Tuple
from algorithms import *

# Creates table in fluids database to store velocity functions and sets up prebuilt functions
with sqlite.Connection("fluids.db") as conn:
    conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS velocity_function (
                written TEXT PRIMARY KEY UNIQUE,
                exponential INTEGER,
                magnitude TEXT,
                argument TEXT);

                INSERT or IGNORE INTO velocity_function VALUES ("tunnel", 1, "1", "pi");
                
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
        self.__flow = False
        self.__velocity_function = ()
        self.__maximum_arrow_length = 0.0

        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_interval = self.__line_height // self.__rows

        x, y = np.meshgrid((np.arange(-self.__line_length//2, self.__line_length//2+1)),np.arange(self.__line_height//2, -self.__line_height//2-1,-1 ))
        self.__plane = np.stack([x, y], axis=-1)
        self.__velocities = np.ones((self.__line_height, self.__line_length, 2))
        
       
    def __drawVector(self, tail_x : int, tail_y : int):
        ...

    def place(self):
        """Draws the vector field"""
        if self.__display:
            # Draws vector field grid and sets up vector arrows
            height = width = self.__maximum_arrow_length = self.__grid_line_interval
            for row in range(self.__rows):
                pygame.draw.line(self.__window, self.__grid_colour, (0, height), (self.__line_length, height))
                height += self.__grid_line_interval
                for i in range(2):
                    for j in range(1, self.__rows):
                        if width == 2*self.__rows*self.__grid_line_interval:
                            break
                    
                        if self.__flow:
                            self.__drawVector(width, self.__grid_line_interval*j)

                    pygame.draw.line(self.__window, self.__grid_colour, (width, 0), (width, self.__line_height))
                    width += self.__grid_line_interval

    def __map(self):
        return
    
    def pointVelocity(self):
        ...

    def __convertFromPygameCoordinate(self, pygame_x, pygame_y):
        """Returns the true possition of a pygame coordinate, with the origin in the centre"""
        return self.__plane[pygame_y][pygame_x]

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