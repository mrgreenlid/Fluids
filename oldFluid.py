import pygame
import numpy as np
from algorithms import *

class VelocityField:
    __PARTICLE_COLOUR = rgbToInt((0,0,0))
    __MAX_PARTICLE_COUNT = 10000
    __PARTICLE_INCREMENT = 300
    __SOURCE_SPACING = 100
    __PARTICLE_SPREAD = 20
    __BG = rgbToInt((255, 255, 255))
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int):
        # Modulate MaxParticleCount in some way
        # Make Mapping a rate not a quota
        self.__screen = screen
        self.__width, self.__height = width, height
        self.__dt = 0.0
    
        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.center = (x, y)

        x, y = np.meshgrid(np.arange(-self.__width//2, self.__width//2), np.arange(self.__height//2, -self.__height//2, -1))
        self.__argand = x + y*1j
        
        self.__plane = pygame.Surface((width, height))
        self.__plane.fill(self.__BG)
        self.__clear = pygame.surfarray.array2d(self.__plane)
        
        self.__current_particle_count = self.__PARTICLE_INCREMENT

        self.__uniform_magnitude = 10
        self.__uniform_argument = np.pi
        self.__velocities = mapUniformFlow(self.__width, self.__height, self.__uniform_magnitude, self.__uniform_argument)

        self.__non_uniform_velocity_function = ""

        self.__lhs_sources = np.column_stack((np.full(shape=(self.__height//self.__SOURCE_SPACING)-1, fill_value=0, dtype=np.int64), np.arange(self.__SOURCE_SPACING, self.__height-1, self.__SOURCE_SPACING)))
        self.__rhs_sources = np.column_stack((np.full(shape=(self.__height//self.__SOURCE_SPACING)-1, fill_value=self.__width-1, dtype=np.int64), np.arange(self.__SOURCE_SPACING, self.__height, self.__SOURCE_SPACING)))
        self.__uhs_sources = np.column_stack((np.arange(self.__SOURCE_SPACING, self.__width-1, self.__SOURCE_SPACING), np.full(shape=(self.__width//self.__SOURCE_SPACING)-1, fill_value=0, dtype=np.int64)))
        self.__dhs_sources = np.column_stack((np.arange(self.__SOURCE_SPACING, self.__width-1, self.__SOURCE_SPACING), np.full(shape=(self.__width//self.__SOURCE_SPACING)-1, fill_value=self.__height-1, dtype=np.int64)))
        self.__all_sources = np.concatenate((self.__lhs_sources, self.__rhs_sources, self.__uhs_sources, self.__dhs_sources))
        self.__available_sources = self.__rhs_sources
        
        self.__particle_positions =  np.full((self.__MAX_PARTICLE_COUNT, 2), -1, dtype=np.int64)
        self.__precise_particle_positions = self.__particle_positions.astype(np.float64)
        
        self.__flow = False
        self.__flow_type = "uniform"

        self.__wave_count = 0

    def place(self):
        """Places the velocity field on the screen"""
        if self.__flow:
            pixels, self.__particle_positions, self.__precise_particle_positions = mapParticles(pygame.surfarray.array2d(self.__plane), self.__particle_positions, self.__precise_particle_positions, self.__velocities, self.__available_sources, self.__PARTICLE_SPREAD, self.__dt, self.__current_particle_count, self.__PARTICLE_COLOUR, self.__BG)

            if self.__current_particle_count < self.__MAX_PARTICLE_COUNT:
                 self.__wave_count += 1
                 if self.__wave_count % 2 == 0:
                     self.__current_particle_count += self.__PARTICLE_INCREMENT
            pygame.surfarray.blit_array(self.__plane, pixels)

        self.__screen.blit(self.__plane, self.__rect)
    
    def uniformFlow(self, magnitude : float, argument : float):
        """Updates attributes for a uniform flow velocity"""
        self.__flow_type = "uniform"
        if magnitude != self.__uniform_magnitude or argument != self.__uniform_argument:
            self.__uniform_magnitude = magnitude
            self.__uniform_argument = argument
            
            self.__velocities = mapUniformFlow(self.__argand, self.__uniform_magnitude, self.__uniform_argument)

            pygame.surfarray.blit_array(self.__plane, self.__clear)
            self.__particle_positions =  np.full((self.__MAX_PARTICLE_COUNT, 2), -1, dtype=np.int64)
            self.__precise_particle_positions = self.__particle_positions.astype(np.float64)
            

    def nonUniformFlow(self, velocity_function : str):
        """Updates attributes for a non uniform flow velocity"""
        self.__flow_type = "non_uniform" 
        if velocity_function != self.__non_uniform_velocity_function:
            self.__non_uniform_velocity_function = velocity_function
            self.__velocities = mapNonUniformFlow(self.__non_uniform_velocity_function)
           

    def flow(self, dt : float):
        """Fluid flows"""
        self.__flow = True
        self.__dt = dt

    def stopFlow(self):
        """Fluid stops flow"""
        self.__flow = False