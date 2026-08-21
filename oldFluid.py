import pygame
import numpy as np
from typing import List, Tuple
from algorithms import *

class Body:
    def __init__(self, window :  pygame.surface.Surface):
        """A body (object)"""
        self.__window = window

        self.__body_index = 0
        self.__fixed = False
        self.pull = False
        self.__rect = pygame.rect.Rect(0,0,0,0)
        self.mask = pygame.mask.Mask((0,0))
        

    def update(self, body_index : int):
        """Updates properties of the body if required"""
        if self.pull:
            self.__rect.centerx, self.__rect.centery = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        
        self.x, self.y = self.__rect.centerx, self.__rect.centery

        if body_index != self.__body_index:
            self.__body_index = body_index
            if body_index == 0:
                self.__mass = 0
                self.__fixed = False
                self.__rect.center = (5000, 5000)
                return None

            properties = getBodyProperties(self.__body_index)
            scale_factor = properties[4]
            self.__mass = properties[3]

            if properties[2] == 1:
                self.__fixed = True
            elif properties[2] == 0:
                self.__fixed = False

            self.__shape = self.__image = pygame.transform.scale_by(pygame.image.load(properties[1]).convert_alpha(), (scale_factor,scale_factor))
            self.mask = pygame.mask.from_surface(self.__shape)
            self.__rect = self.__shape.get_rect()
            self.__rect.centerx, self.__rect.centery = self.__window.get_width()//2, self.__window.get_height()//2


    def place(self):
        """Places the body on the screen"""
        if self.__body_index != 0:
            self.__window.blit(self.__shape, self.__rect)
            
    
    def checkInteract(self, event):
        """Checks for interactions"""
        if self.__body_index != 0:
            if not self.__fixed:
                mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                if self.__rect.collidepoint(mouse_x, mouse_y):
                    if self.mask.get_at((mouse_x-self.__rect.x, mouse_y-self.__rect.y)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.pull = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pull = False
                    
    






    
class VectorField(Output):
    __grid_colour =  "#C7C1B8"
    __variables = ["show_field", "field_rows", "flow", "speed"]
    def __init__(self, window : pygame.surface.Surface, display : bool = False, rows : int = 10,  flow : bool = False, speed : float = 1.0):
        """A velocity vector field"""
        self.__window = window

        self.__display = display
        self.__rows = rows
        self.__flow = flow
        self.__speed = speed
        self.__body = ""

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
                        try: 
                            flag = self.__body.mask.get_at((x-self.__body.x,y-self.__body.y))
                        except:
                            self.__drawVector(x,y)
    


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

    def linkBody(self, body : Body):
        self.__body = body

    def getVariable(self):
        """Returns associated variable"""
        return self.__variables
    
    def setValue(self, display, rows, flow, speed):
        """Changes variable value"""
        self.__display = display
        self.__flow = flow
        
        if speed != self.__speed:
            self.__speed = speed
            self.__mapVelocities()

        if self.__rows != rows:
            self.__rows = rows
            self.__grid_line_interval = self.__height // self.__rows
            self.__maximum_arrow_length = self.__grid_line_interval * 0.7
        




class Particle(pygame.sprite.Sprite):
    def __init__(self, window : pygame.surface.Surface, start_side, vector_field : VectorField):
        """A fluid particle"""
        ...