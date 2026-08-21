import pygame
from algorithms import *
import numpy as np
from typing import Tuple
import re
import cmath

class VectorField(Output):
    __grid_colour = "#C7C1B8"
    __variables = ["show_field", "field_rows", "flow", "speed"]
    def __init__(self, screen : pygame.surface.Surface, show : bool = False, rows : int = 10, flow : bool = False):
        """A fluid velocity vector field"""
        self.__screen = screen
        self.__show = show
        self.__rows = rows
        self.__flow = flow
        self.__speed = 1
    
        self.__velocity_function = ()

        self.__eMagnitude = 0
        self.__eArgument = 0

        self.__width = screen.get_width()
        self.__height = screen.get_height()
        self.__grid_line_interval = self.__height // self.__rows
        self.__maximum_arrow_length = self.__grid_line_interval * 0.7

        x, y = np.meshgrid((np.arange(-self.__width//2, self.__width//2+1)),np.arange(self.__height//2, -self.__height//2-1, -1))
        self.__plane = x + y*1j
        self.__velocities = np.zeros((self.__height, self.__width), dtype=np.complex128)

    def place(self):
        """Places the vector field on the screen"""
        if self.__show:
            for row in range(self.__rows+1):
                y_line= row*self.__grid_line_interval
                pygame.draw.line(self.__screen, self.__grid_colour, (0, y_line), (self.__width, y_line))
        
            for column in range(self.__rows*2+1):
                x_line = column * self.__grid_line_interval
                pygame.draw.line(self.__screen, self.__grid_colour, (x_line, 0), (x_line, self.__height))
            
            if self.__flow:
                for row in range(self.__rows+1):
                    for column in range(self.__rows*2+1):
                        x = column * self.__grid_line_interval
                        y = row * self.__grid_line_interval
                        self.__drawVector(x, y)

    def __drawVector(self, x : int, y : int):
        """Draws a vector"""
        velocity = self.getPointVelocity(x, y)
        if abs(velocity) != 0:
            arrow_points = translate(rotate(np.array([(self.__maximum_arrow_length, 0), 
                                                    (0.6*self.__maximum_arrow_length, 0.2*self.__maximum_arrow_length),
                                                    (0.6*self.__maximum_arrow_length, -0.2*self.__maximum_arrow_length)], dtype=np.float64), cmath.phase(velocity)), x, y)
        
            vector_colour = colourByMagnitude(abs(velocity))
            pygame.draw.line(self.__screen,vector_colour, (x, y), (arrow_points[0][0], arrow_points[0][1]))
            pygame.draw.polygon(self.__screen, vector_colour, arrow_points)

    def getPointVelocity(self, x : int | float, y : int | float):
        """Returns the velocity at a point on the field"""
        return self.__velocities[round(y-1)][round(x-1)]

    def __mapExponential(self):
        """Cements changes made to field attributes"""
        self.__velocities = np.ones((self.__height, self.__width), dtype=np.complex128)
        complex_point = self.__eMagnitude*np.cos(self.__eArgument) + 1j*self.__eMagnitude*np.sin(self.__eArgument)
        self.__velocities *= complex_point*self.__speed


    def updateFunction(self, function : Tuple[str]):
        """Updates the velocity function of the field"""
        if function != self.__velocity_function:
            self.__velocity_function = function

            # Finds attributes of an exponential form function
            if self.__velocity_function[0] == 1:
                
                self.__eMagnitude = float(self.__velocity_function[1])
                argument = 1

                arg = re.split(r"(\*|\/)", self.__velocity_function[2])
                for term in range(1, len(arg), 2):
                    if arg[term+1] == ")":
                        break
                    if arg[term] == "*":
                        if arg[term+1] == "pi":
                            argument *= np.pi
                        else:
                            argument *= float(arg[term+1])
                    elif arg[term] == "/":
                        if arg[term+1] == "pi":
                            argument /= np.pi
                        else:
                            argument /= float(arg[term+1])
                self.__eArgument = argument
                self.__mapExponential()
                
    def getVariable(self):
        """Returns associated variables"""
        return self.__variables

    def update(self, show, rows, flow, speed):
        """Updates variables"""
        self.__show = show
        self.__flow = flow

        if self.__rows != rows:
            self.__rows = rows
            self.__grid_line_interval = self.__height // self.__rows
            self.__maximum_arrow_length = self.__grid_line_interval * 0.7
        
        if speed != self.__speed:
            self.__speed = speed
            self.__mapExponential()
            
           
        
