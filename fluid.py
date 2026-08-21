import pygame
from algorithms import *
import databaseManagement as db
import numpy as np
from typing import Tuple
import re
import cmath


class Body:
    def __init__(self, screen : pygame.surface.Surface):
        """A pygame body"""
        self.__screen = screen

        self.__body_index = 0
        self.__fixed = True
        self.__pull = False

        self.__rect = pygame.rect.Rect(0,0,0,0)
        self.mask = pygame.mask.Mask((0,0))
        
    def update(self, body_index : int):
        """Updates the bodies attributes"""
        if self.__pull:
            self.__rect.center = (*pygame.mouse.get_pos(),)

        if body_index != self.__body_index:
            self.__body_index = body_index
            properties = db.getBodyProperties(self.__body_index)
            self.__mass = properties[3]

            if properties[2] == 1:
                self.__fixed = True
            else:
                self.__fixed = False

            self.__shape = pygame.transform.scale_by(pygame.image.load(properties[1]), (properties[4], properties[4]))
            self.__rect = self.__shape.get_rect()
            self.__rect.center = (self.__screen.get_width()//2, self.__screen.get_height()//2)
            self.mask = pygame.mask.from_surface(self.__shape)

    def place(self):
        """Places the body on the screen"""
        self.__screen.blit(self.__shape, self.__rect)

    def checkInteract(self, event):
        """Checks for interactions"""
        if not self.__fixed:
            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            if self.__rect.collidepoint(mouse_x, mouse_y):
                if self.mask.get_at((mouse_x-self.__rect.x, mouse_y-self.__rect.y)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.__pull = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.__pull = False          

    def collide(self, x : int, y : int):
        """Checks if the body collides with a point"""
        if self.__rect.collidepoint(x, y):
            if self.mask.get_at((x-self.__rect.x, y-self.__rect.y)):
                return True
        return False


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

        self.__body = None
    
        self.__velocity_function = ()

        self.__exponential_magnitude = 0
        self.__exponential_argument = 0

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
        
            if not (self.__body.collide(x, y) or self.__body.collide(arrow_points[0][0], arrow_points[0][1])):
            
                vector_colour = colourByMagnitude(abs(velocity))
                pygame.draw.line(self.__screen,vector_colour, (x, y), (arrow_points[0][0], arrow_points[0][1]))
                pygame.draw.polygon(self.__screen, vector_colour, arrow_points)

    def getPointVelocity(self, x : int | float, y : int | float):
        """Returns the velocity at a point on the field"""
        return self.__velocities[round(y-1)][round(x-1)]

    def __mapExponential(self):
        """Cements changes made to field attributes"""
        self.__velocities = np.ones((self.__height, self.__width), dtype=np.complex128)
        complex_point = self.__exponential_magnitude*np.cos(self.__exponential_argument) + 1j*self.__exponential_magnitude*np.sin(self.__exponential_argument)
        self.__velocities *= complex_point*self.__speed

    def linkBody(self, body : Body):
        self.__body = body

    def updateFunction(self, function : Tuple[str]):
        """Updates the velocity function of the field"""
        if function != self.__velocity_function:
            self.__velocity_function = function

            # Finds attributes of an exponential form function
            if self.__velocity_function[0] == 1:
                
                self.__exponential_magnitude = float(self.__velocity_function[1])
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
                self.__exponential_argument = argument
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
            
           
        
