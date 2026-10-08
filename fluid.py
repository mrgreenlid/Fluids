import pygame
import numpy as np
from algorithms import *

class VelocityField:
    __BG = rgbToInt((255, 255, 255))
    __PARTICLE_COLOUR = rgbToInt((0,0,0))
    __PARTICLE_COUNT = 10000
    __MINIMUM_MAG = 5
    __MAXIMUM_MAG = 1000
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int):
        """A fluid velocity field"""
        self.__screen = screen
        self.__width, self.__height = width, height
    
        self.__dt = float

        self.__rect = pygame.Rect(0,0, self.__width, self.__height)
        self.__rect.center = (x, y)

        x_coords = np.arange(-self.__width//2, self.__width//2)
        y_coords = np.arange(self.__height//2, -self.__height//2)
        real, imag = np.meshgrid(x_coords, y_coords)
        self.__argand = real + imag*1j  

        self.__plane = pygame.Surface((width, height))
        self.__plane.fill(self.__BG)
        
        self.__particle_positions = np.full((self.__PARTICLE_COUNT, 2), -1, dtype=np.float64)

        self.__uniform_magnitude = float(10)
        self.__uniform_argument = np.pi

        self.__non_uniform_flow_name = str

        self.__velocities = mapUniformFlow(self.__uniform_magnitude, self.__uniform_argument, width, height)
        self.__flow = False

        self.clearAndFill()

    def place(self):
        """Places the velocity field on the screen"""
        if self.__flow:
            pixels, self.__particle_positions = mapParticles(pygame.surfarray.array2d(self.__plane), self.__particle_positions, self.__velocities, self.__dt, self.__PARTICLE_COUNT, self.__PARTICLE_COLOUR, self.__BG)
            pygame.surfarray.blit_array(self.__plane, pixels)
        self.__screen.blit(self.__plane, self.__rect)
        
    def uniformFlow(self, magnitude : float, argument : float):
        """Updates attributes for a uniform velocity flow"""
        self.__uniform_argument = argument
        if magnitude < self.__MINIMUM_MAG:
            magnitude = self.__MINIMUM_MAG
        elif magnitude > self.__MAXIMUM_MAG:
            magnitude = self.__MAXIMUM_MAG 
        self.__uniform_magnitude = magnitude
        self.__velocities = mapUniformFlow(self.__uniform_magnitude, self.__uniform_argument, self.__width, self.__height)
        self.clearAndFill()
        
    def nonUniformFlow(self, flow_name : str):
        """Updates attributes for a non uniform velocity flow"""
        self.__non_uniform_flow_name = flow_name
        self.clearAndFill()

    def clearAndFill(self):
        """Fills the velocity field with particles"""
        pixels, self.__particle_positions = fillScreen(self.__PARTICLE_COUNT, self.__width, self.__height, self.__PARTICLE_COLOUR, self.__BG)
        pygame.surfarray.blit_array(self.__plane, pixels)

    def flow(self, dt):
        """Flow"""
        self.__flow = True
        self.__dt = dt
        
    def stopFlow(self):
        """Stop flow"""
        self.__flow = False