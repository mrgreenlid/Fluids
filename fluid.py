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
                INSERT or IGNORE INTO velocity_function VALUES ("vortex", 1, "1", "pi*0.25");
                INSERT or IGNORE INTO velocity_function VALUES ("falling", 1, "1", "pi*0.5");

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

        self.__speed = 1
        self.__velocity_function = []
        self.__magnitude = ""
        self.__argument = ""
        self.__exponential = False

        self.__q = ()
    
        self.__line_length = window.get_width()
        self.__line_height = window.get_height()
        self.__grid_line_interval = self.__line_height // self.__rows
        self.__maximum_arrow_length = self.__grid_line_interval * 0.6
        
        x, y = np.meshgrid((np.arange(-self.__line_length//2, self.__line_length//2+1)),np.arange(self.__line_height//2, -self.__line_height//2-1, -1))
        self.__plane = x + y*1j
        self.__velocities = np.zeros((self.__line_height, self.__line_length), dtype=np.complex128)
        

    def __drawVector(self, tail_pygame_x : int, tail_pygame_y : int):
        """Draws coloured vector arrow with the tail at the specified point"""
        velocity = self.pointVelocity(tail_pygame_x, tail_pygame_y)
        dx, dy = velocity.real, velocity.imag
        scale_factor = np.sqrt( (self.__maximum_arrow_length**2)/(dx**2 +dy**2) )
        tip_pygame_x, tip_pygame_y = tail_pygame_x + dx*scale_factor, tail_pygame_y - dy*scale_factor

       


        vector_colour = self.__colourByMagnitude(np.sqrt(dx**2+dy**2))

        pygame.draw.line(self.__window,vector_colour, (tail_pygame_x, tail_pygame_y), (tip_pygame_x, tip_pygame_y))
        #pygame.draw.polygon(self.__window, vector_colour, arrow_points)

    def place(self):
        """Draws the vector field"""
        # Draws vector field grid and sets up vector arrows
        if self.__display:
            for row in range(self.__rows+1):
                y_line= row*self.__grid_line_interval
                pygame.draw.line(self.__window, self.__grid_colour, (0, y_line), (self.__line_length, y_line))
        
            for column in range(self.__rows*2):
                x_line = column * self.__grid_line_interval
                pygame.draw.line(self.__window, self.__grid_colour, (x_line, 0), (x_line, self.__line_height))

            if self.__flow:
                for row in range(1, self.__rows):
                    for column in range(1, self.__rows*2):
                        x = column * self.__grid_line_interval
                        y = row * self.__grid_line_interval
                        self.__drawVector(x, y)

    def __map(self):
        """Updates the velocities array for each point"""
        if self.__exponential:
            self.__velocities = np.ones((self.__line_height, self.__line_length), dtype=np.complex128)
            self.__velocities *= complex(real= self.__magnitude*np.cos(self.__argument), imag= self.__magnitude*np.sin(self.__argument))*self.__speed

    def pointVelocity(self, pygame_x, pygame_y):
        """Returns the velocity at a specific point on the field"""
        return self.__velocities[pygame_y-1][pygame_x-1]

    def __convertFromPygameCoordinate(self, pygame_x, pygame_y):
        """Returns the true possition of a pygame coordinate, with the origin in the centre"""
        return self.__plane[pygame_y-1][pygame_x-1]

    def __colourByMagnitude(self, magnitude):
        """Returns a hex value for a temperature colour based on a given magnitude"""
        colour = "#0000ff"
        return colour


    

    def setVelocityFunction(self, velocity_function : Tuple[str] | Tuple[int]):
        """Updates the velocity function of the vector field"""
        if self.__q != velocity_function:
            self.__q = velocity_function
            self.__velocity_function = list(velocity_function)
            
            if self.__velocity_function[0] == 1:
                argument = 1
                for term in self.__velocity_function[2].split("*"):
                    if term == "pi":
                        argument *= np.pi
                    else:
                        argument *= float(term)
                self.__velocity_function[2] = argument
                self.__velocity_function[1] = float(self.__velocity_function[1])

                self.__exponential = True
                self.__magnitude = self.__velocity_function[1]
                self.__argument = self.__velocity_function[2]

            self.__map()

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    def setValue(self, display, rows, flow, speed):
        """Changes variable value"""
        self.__display = display
        self.__flow = flow
        
        if speed != self.__speed:
            self.__speed = speed
            self.__map()

        if self.__rows != rows:
            self.__rows = rows
            self.__grid_line_interval = self.__line_height // self.__rows
            self.__maximum_arrow_length = self.__grid_line_interval * 0.6
        


class Particle(pygame.sprite.Sprite):
    def __init__(self,):
        return 

class Body(pygame.sprite.Sprite):
    def __init__(self,):
        return