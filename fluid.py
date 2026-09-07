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
        self.__mask = pygame.mask.Mask((0,0))

        self.__streamline = False
        
    def update(self, body_index : int, show_streamline : bool = False):
        """Updates the body's attributes"""
        if self.__pull:
            self.__rect.center = (*pygame.mouse.get_pos(),)

        if body_index != self.__body_index:
            self.__body_index = body_index
            if self.__body_index == 0:
                return None

            properties = db.getBodyProperties(self.__body_index)
            self.__mass = properties[3]

            if properties[2] == 1:
                self.__fixed = True
            else:
                self.__fixed = False

            
            self.__shape = pygame.transform.scale_by(pygame.image.load(properties[1]), (properties[4], properties[4]))
            self.__rect = self.__shape.get_rect()
            self.__rect.center = (self.__screen.get_width()//2, self.__screen.get_height()//2)
            self.__mask = pygame.mask.from_surface(self.__shape)
        
        self.__streamline = show_streamline

    def place(self):
        """Places the body on the screen"""
        if self.__streamline:
            # Constantly add to a group of coords and draw pygame line from them
            ...
        if self.__body_index != 0:
            self.__screen.blit(self.__shape, self.__rect)
        

    def checkInteract(self, event):
        """Checks for interactions"""
        if not self.__fixed:
            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            if self.__rect.collidepoint(mouse_x, mouse_y):
                if self.__mask.get_at((mouse_x-self.__rect.x, mouse_y-self.__rect.y)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.__pull = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.__pull = False          

    def collide(self, x : int, y : int):
        """Checks if the body collides with a point"""
        if self.__body_index != 0:
            if self.__rect.collidepoint(x, y):
                if self.__mask.get_at((x-self.__rect.x, y-self.__rect.y)):
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
        self.exponential = None
        self.exponential_magnitude = 0
        self.exponential_argument = 0

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
        return self.__velocities[y-1][x-1]
        
    def __mapExponential(self):
        """Cements changes made to field attributes"""
        self.__velocities = np.ones((self.__height, self.__width), dtype=np.complex128)
        complex_point = self.exponential_magnitude*np.cos(self.exponential_argument) + 1j*self.exponential_magnitude*np.sin(self.exponential_argument)
        self.__velocities *= complex_point*self.__speed

    def linkBody(self, body : Body):
        """Links a body to the field"""
        self.__body = body
        
    def updateFunction(self, function : Tuple[str]):
        """Updates the velocity function of the field"""
        if function != self.__velocity_function:
            self.__velocity_function = function

            # Finds attributes of an exponential form function
            if self.__velocity_function[0] == 1:
                self.exponential = True
                
                self.exponential_magnitude = float(self.__velocity_function[1])
                argument = 1
                arg = re.split(r"(\*|\/)", self.__velocity_function[2])
                for term in range(1, len(arg), 2):
                    if arg[term+1] == ")":
                        break
                    if arg[term] == "*":
                        if re.match(r"pi", arg[term+1]):
                            argument *= np.pi
                        else:
                            argument *= float(arg[term+1])

                    elif arg[term] == "/":
                        if re.match(r"pi", arg[term+1]):
                            argument /= np.pi
                        else:
                            argument /= float(arg[term+1])

                self.exponential_argument = argument
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

            if self.exponential:
                self.__mapExponential()
            

class Source:
    def __init__(self, screen : pygame.surface.Surface):
        """A pygame fluid source"""
        self.__screen = screen
        self.__vector_field = None
        self.__screen_height, self.__screen_width = self.__screen.get_height(), self.__screen.get_width()
        slit_spacing = 20

        # Defines the location of every possible slit
        self.__lhs_slits = np.column_stack((np.full(shape=(self.__screen_height//slit_spacing)-1, fill_value=0, dtype=np.int64), np.arange(slit_spacing, self.__screen_height, slit_spacing)))
        self.__rhs_slits = np.column_stack((np.full(shape=(self.__screen_height//slit_spacing)-1, fill_value=self.__screen_width, dtype=np.int64), np.arange(slit_spacing, self.__screen_height, slit_spacing)))
        self.__uhs_slits = np.column_stack((np.arange(slit_spacing, self.__screen_width, slit_spacing), np.full(shape=(self.__screen_width//slit_spacing)-1, fill_value=0, dtype=np.int64)))
        self.__dhs_slits = np.column_stack((np.arange(slit_spacing, self.__screen_width, slit_spacing), np.full(shape=(self.__screen_width//slit_spacing)-1, fill_value=self.__screen_height, dtype=np.int64)))

        self.available_slits = self.__all_slits = np.concatenate((self.__lhs_slits, self.__rhs_slits, self.__uhs_slits, self.__dhs_slits))
    
        self.__scout_coords = np.array([(0,0), (np.sqrt(self.__screen_height**2 + self.__screen_width**2), 0)])

    def update(self):
        """Updates the current sources"""
        if not self.__vector_field.exponential:
            self.available_slits = self.__all_slits

        else:
            positive = False
            if self.__vector_field.exponential_argument > 0:
                positive = True

            theta = self.__vector_field.exponential_argument-np.pi/2
            scout = rotate(self.__scout_coords, theta)

            base = (self.__screen_width//2,self.__screen_height)

            # if positive:
            #     self.available_slits = np.array([])
            #     for slit in self.__all_slits:
            #         print(base[1] - base[0]*np.tan(theta))
            #         if base[1] - base[0]*np.tan(theta) < slit[0] - slit[1]*np.tan(theta):
            #             np.append(self.available_slits, slit)

            # MAKE THE SCOUT WORK 

           
            
    def linkVectorField(self, vector_field : VectorField):
        """Links a vector field to the fluid source"""
        self.__vector_field = vector_field





class Particle(pygame.sprite.Sprite):
    __width = 1
 
    def __init__(self, screen : pygame.surface.Surface, vector_field : VectorField, source : Source):
        super().__init__()
        self.__screen = screen
        self.__vector_field = vector_field
        self.__source = source

        self.__boundx, self.__boundy = screen.get_width(), screen.get_height()
        self.__rect = pygame.rect.Rect(self.__boundx//2, self.__boundy//2, self.__width, self.__width)

    def place(self):
        pygame.draw.rect(self.__screen, "#000000", self.__rect)

    def update(self):
        if not (0 <= self.__rect.centerx <= self.__boundx) or not (0 <= self.__rect.centery <= self.__boundy):
                self.__relocate()
                return None

        velocity = self.__vector_field.getPointVelocity(self.__rect.centerx, self.__rect.centery)
        self.__rect.centerx += velocity.real
        self.__rect.centery -= velocity.imag
        self.place()

    def __relocate(self):
        new_slit = randomChoice(self.__source.available_slits)
        self.__rect.centerx, self.__rect.centery = new_slit[0], new_slit[1] 
        
            



                

