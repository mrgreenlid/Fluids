import pygame
import numpy as np
from algorithms import mapUniformFlow, drawParticles


class VelocityField:
    __SLIT_SPACING = 50
    __PARTICLE_COLOUR = (0,0,0)
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int):
        self.__screen = screen
        self.__width, self.__height = width, height

        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.center = (x, y)

        x, y = np.meshgrid(np.arange(-self.__width//2, self.__width//2), np.arange(self.__height//2, -self.__height//2, -1))
        self.__argand = x + y*1j
        self.__velocities = np.empty((self.__height, self.__width), dtype=np.complex64)

        self.__plane = pygame.Surface((width, height))
        self.__plane.fill("#FFFFFF")
        
        self.__flow = False
        self.__flow_type = "uniform"

        self.__uniform_magnitude = 1
        self.__uniform_angle = np.pi

        self.__lhs_slits = np.column_stack((np.full(shape=(self.__height//self.__SLIT_SPACING)-1, fill_value=0, dtype=np.int64), np.arange(self.__SLIT_SPACING, self.__height, self.__SLIT_SPACING)))
        self.__rhs_slits = np.column_stack((np.full(shape=(self.__height//self.__SLIT_SPACING)-1, fill_value=self.__width, dtype=np.int64), np.arange(self.__SLIT_SPACING, self.__height, self.__SLIT_SPACING)))
        self.__uhs_slits = np.column_stack((np.arange(self.__SLIT_SPACING, self.__width, self.__SLIT_SPACING), np.full(shape=(self.__width//self.__SLIT_SPACING)-1, fill_value=0, dtype=np.int64)))
        self.__dhs_slits = np.column_stack((np.arange(self.__SLIT_SPACING, self.__width, self.__SLIT_SPACING), np.full(shape=(self.__width//self.__SLIT_SPACING)-1, fill_value=self.__height, dtype=np.int64)))

        self.__available_slits = self.__all_slits = np.concatenate((self.__lhs_slits, self.__rhs_slits, self.__uhs_slits, self.__dhs_slits))



    
        
    def place(self):
        """Places the velocity field on the screen"""
        if self.__flow:
            drawParticles(pygame.surfarray.array2d(self.__plane), self.__velocities)


        self.__screen.blit(self.__plane, self.__rect)
    
    def pygameToArgand(self, x : int, y : int):
        """Converts a pygame coordinate to a complex coordinate"""
        return self.__argand[y][x]

    def uniformFlow(self, magnitude : float, angle : float):
        """Updates attributes for a uniform flow velocity"""
        if self.__flow_type != "uniform":
            self.__flow_type = "uniform"
            self.__uniform_magnitude = magnitude
            self.__uniform_angle = angle
            mapUniformFlow(self.__argand, self.__uniform_magnitude, self.__uniform_angle)

    def nonUniformFlow(self):
        """Updates attributes for a non uniform flow velocity"""
        self.__flow_type = "non_uniform" 

    def flow(self):
        """Fluid flows"""
        self.__flow = True

    def stopFlow(self):
        """Fluid stops flow"""
        self.__flow = False