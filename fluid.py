import pygame
import numpy as np




class velocityFunction:
    def __init__(self):
        return





class VectorField:
    def __init__(self, window : pygame.surface.Surface, rows : int):
        self.__field = np.empty((window.get_height(), window.get_width()), dtype = np.float64)
        self.__rows = rows

        self.__line_width = window.get_width()
        self.__line_height = window.get_height()

    def __addVector():
        return

    def update():
        return

    def place():
        current = self.__line_height//rows
        for row in range(rows):
            pygame.draw.line(window, "#000000", (0, current),(self.__line_width, current))
            current += current
        


        
class Particle(pygame.sprite.Sprite):
    def __init__(self,):

        return 

class Body(pygame.sprite.Sprite):
    def __init__(self,):
        return