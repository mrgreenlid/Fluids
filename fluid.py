import pygame
import numpy as np
from typing import List, Tuple
from algorithms import *


    
class VectorField(Output):
    __grid_colour =  "#C7C1B8"
    __variables = ["show_field", "field_rows", "flow", "speed", "dt"]
    def __init__(self, window : pygame.surface.Surface, display : bool = False, rows : int = 10,  flow : bool = False, speed : float = 1.0):
        """Creates a vector field to be displayed and store data"""
        self.__window = window

        self.__display = display
        self.__rows = rows
        self.__flow = flow
        self.__speed = speed

        self.__velocity_function = []
        self.__q = ()
    
        self.__argument = ""

        self.__length = window.get_width()
        self.__height = window.get_height()
        self.__grid_line_interval = self.__height // self.__rows
        self.__maximum_arrow_length = self.__grid_line_interval * 0.7
        
        x, y = np.meshgrid((np.arange(-self.__length//2, self.__length//2+1)),np.arange(self.__height//2, -self.__height//2-1, -1))
        self.__plane = x + y*1j
        self.__velocities = np.zeros((self.__height, self.__length), dtype=np.complex128)
        
        self.__delta_time = 1
    def __drawVector(self, tail_pygame_x : int, tail_pygame_y : int):
        """Draws coloured vector arrow with the tail at the specified point"""
        velocity = self.getPointVelocity(tail_pygame_x, tail_pygame_y)

        if abs(velocity) != 0:
            # Add some vector Wobble
            arrow_points = translate(rotate(np.array([(self.__maximum_arrow_length, 0), 
                                                    (0.6*self.__maximum_arrow_length, 0.2*self.__maximum_arrow_length),
                                                    (0.6*self.__maximum_arrow_length, -0.2*self.__maximum_arrow_length)], dtype=np.float64), self.__argument), tail_pygame_x, tail_pygame_y)
        
            vector_colour = colourByMagnitude(abs(velocity))
                        
            pygame.draw.line(self.__window,vector_colour, (tail_pygame_x, tail_pygame_y), (arrow_points[0][0], arrow_points[0][1]))
            pygame.draw.polygon(self.__window, vector_colour, arrow_points)



    def place(self):
        """Draws the vector field and arrows if relevant"""
        # Draws vector field grid and sets up vector arrows
        if self.__display:
            for row in range(self.__rows+1):
                y_line= row*self.__grid_line_interval
                pygame.draw.line(self.__window, self.__grid_colour, (0, y_line), (self.__length, y_line))
        
            for column in range(self.__rows*2+1):
                x_line = column * self.__grid_line_interval
                pygame.draw.line(self.__window, self.__grid_colour, (x_line, 0), (x_line, self.__height))

            if self.__flow:
                for row in range(self.__rows+1):
                    for column in range(self.__rows*2+1):
                        x = column * self.__grid_line_interval
                        y = row * self.__grid_line_interval
                        self.__drawVector(x, y)


    def __mapVelocities(self):
        self.__velocities = mapVelocities(*self.__velocity_function, self.__height, self.__length, self.__speed)


    def getPointVelocity(self, pygame_x, pygame_y):
        """Returns the velocity at a specific point on the field"""
        return self.__velocities[round(pygame_y-1)][round(pygame_x-1)]


    def __convertFromPygameCoordinate(self, pygame_x, pygame_y):
        """Returns the true possition of a pygame coordinate, with the origin in the centre"""
        return self.__plane[pygame_y-1][pygame_x-1]


    def updateVelocityFunction(self, velocity_function : Tuple[str]):
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
                self.__argument = argument
                self.__velocity_function[1] = float(self.__velocity_function[1])
                
            self.__mapVelocities()

    def getVariable(self):
        """Returns associated variable"""
        return self.__variables
    
    def setValue(self, display, rows, flow, speed, dt):
        """Changes variable value"""
        self.__display = display
        self.__flow = flow
        self.__delta_time = dt
        
        
        
        if speed != self.__speed:
            self.__speed = speed
            self.__mapVelocities()

        if self.__rows != rows:
            self.__rows = rows
            self.__grid_line_interval = self.__height // self.__rows
            self.__maximum_arrow_length = self.__grid_line_interval * 0.7
        




class Particle(pygame.sprite.Sprite):
    def __init__(self, window: pygame.surface.Surface, start_side, vector_field : VectorField):
        """A fluid particle"""
        self.__window = window
        self.__vector_field = vector_field

        self.__initial_x, self.__inital_y, self.__x, self.__y = x, y
        
        self.__colour = "#000000"

            
    def update(self, delta_time : pygame.time.Clock.tick):
        velocity = self.__vector_field.getPointVelocity(self.__x, self.__y)
        ...
    
    
    def place(self):
        ...




class Body():
    def __init__(self,):
        ...