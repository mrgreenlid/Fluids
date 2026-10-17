import pygame
import numpy as np
import arrayMath as am
import interfaceMath as im
import databaseManagement as db


class VelocityField:

    __BG_COLOUR = 16777215
    __PARTICLE_COLOUR = 0
    __PARTICLE_COUNT = 50000

    def __init__(self, screen : pygame.Surface, x : int, y : int, width : int, height : int):
        """A fluid's velocity field"""

        self.__screen = screen
        self.__width = width
        self.__height = height
        self.__dt = float

        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.center = (x, y)

        x_coords = np.arange(-self.__width//2, self.__width//2)
        y_coords = np.arange(self.__height//2, -self.__height//2, -1)
        y, x = np.meshgrid(y_coords, x_coords)
        self.__argand = x + y*1j

        self.__plane = pygame.Surface((self.__width, self.__height))
        self.__plane.fill(self.__BG_COLOUR)
        self.__empty_plane = pygame.surfarray.array2d(self.__plane)

        self.__particle_positions = np.full((self.__width, self.__height, 2), -1, dtype=np.float64)
        
        self.__uniform = True

        self.__uniform_magnitude = 10.0
        self.__uniform_argument = np.pi
       
        self.__non_uniform_velocity_function = str
        self.__non_uniform_flow_name = str
       
        self.__velocities = am.mapUniformVelocity(self.__uniform_magnitude, self.__uniform_argument, self.__width, self.__height)
        self.__flow = False

        self.__fill()


    def place(self):
        """Places the velocity field on the screen"""
        if self.__flow:
            self.__particle_positions = am.moveParticles(self.__particle_positions, self.__velocities, self.__dt, self.__uniform)
            pixels = am.pixelArray(self.__particle_positions, self.__empty_plane, 0)
            pygame.surfarray.blit_array(self.__plane, pixels)
        self.__screen.blit(self.__plane, self.__rect)

    def uniformFlow(self, magnitude : float, argument : float):
        """Updates attributes for a uniform flow"""
        self.__uniform = True
        self.__uniform_magnitude = magnitude
        self.__uniform_argument = argument
        self.__velocities = am.mapUniformVelocity(self.__uniform_magnitude, self.__uniform_argument, self.__width, self.__height)
        self.__fill()

    def nonUniformFlow(self, flow_name : str):
        """Updates attributes for a non uniform flow"""
        self.__uniform = False
        flow = db.getFlowAttributes(flow_name)
        self.__non_uniform_flow_name = flow[0]
        self.__non_uniform_velocity_function, z_positions = im.naturaliseFlowFunction(flow[1])
        self.__non_uniform_source_x = flow[2]
        self.__non_uniform_source_y = flow[3]
        displacement_scalar = flow[4]
        self.__velocities = am.mapNonUniformVelocity(self.__non_uniform_velocity_function, z_positions, self.__argand, displacement_scalar)
        self.__fill()
        
    def __fill(self):
        """Fills the field, randomly, with particles"""
        self.__particle_positions = am.mapFilledScreen(self.__particle_positions, self.__PARTICLE_COUNT)
        pixels = am.pixelArray(self.__particle_positions, self.__empty_plane, 0)
        pygame.surfarray.blit_array(self.__plane, pixels)

    def flowState(self, flow : bool, dt : float = None):
        """Sets the state of fluid flow"""
        if flow:
            self.__flow = True
            self.__dt = dt
        else:
            self.__flow = False


