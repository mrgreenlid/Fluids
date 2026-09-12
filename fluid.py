import pygame
import numpy as np

class VelocityField:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int):
        self.__screen = screen
        self.__width, self.__height = width, height

        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.center = (x, y)

        x, y = np.meshgrid(np.arange(-self.__width//2, self.__width//2), np.arange(self.__height//2, -self.__height//2, -1))
        self.__argand = x + y*1j
        self.__velocities = np.zeros((self.__height, self.__width), dtype=np.complex64)

        self.__plane = pygame.Surface((width, height))
        self.__plane.fill("#FFFFFF")
        self.__pixels = pygame.surfarray.array2d(self.__plane)
        
        
        
        

    
        
    
    

    def place(self):
        """Places the velocity field on the screen"""  
        self.__screen.blit(self.__plane, self.__rect)

    def pygameToArgand(self, x : int, y : int):
        """Converts a pygame coordinate to a complex coordinate"""
        return self.argand[y][x]

