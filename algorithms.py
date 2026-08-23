import pygame
from typing import List
import numpy as np
import numba as nb
import re


# Pygame interaction statuses
class Output:
    def __init__(self):
        """Defines an object as taking variables to perform a task"""
        return None

class Input:
    def __init__(self):
        """Defines an object as providing variables to perform a task"""
        return None
        
# Pygame specific algorithms
def tapping(event : pygame.event.Event):
    """Returns True when a left click is detected, else False"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    return False

def typing(event : pygame.event.Event):
    """Returns True when any keypress is detected, else False"""
    if event.type == pygame.KEYDOWN:
        return True
    return False

@nb.njit
def rotate(point : np.array, radians : float):
    """Rotates a point or group of points about the origin"""
    radians *= -1
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                [np.sin(radians), np.cos(radians)]], dtype=np.float64)
    
    return point @ rotation_matrix.T

@nb.njit
def translate(point : np.array, dx : int, dy : int):
    """Translates np.array group of coordinates"""
    for dot in range(point.shape[0]):
        point[dot][0] += dx
        point[dot][1] += dy
    return point

COLOURS = np.array([(0,0,255),(13,0,242),(26,0,229),(39,0,216),(52,0,203),(65,0,190),
(78,0,177),(91,0,164),(104,0,151),(117,0,138),(130,0,125),(143,0,112),(156,0,99),
(169,0,86),(182,0,73),(195,0,60),(208,0,47),(221,0,34),(234,0,21),(247,0,8),(255,0,0)], dtype=np.float64)

PARAMETERS = np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100], dtype=np.float64)

@nb.njit
def colourByMagnitude(magnitude: float):
    """Returns an RGB value for a temperature colour based on a given magnitude"""
    value = round(magnitude)

    position = np.searchsorted(PARAMETERS, value)

    if value >= PARAMETERS[-1]:
        return COLOURS[-1]

    elif value <= PARAMETERS[0]:
        return COLOURS[0]

    higher_parameter = PARAMETERS[position]
    lower_parameter = PARAMETERS[position-1]

    higher_colour = COLOURS[position]
    lower_colour = COLOURS[position-1]

    proportion = (value-lower_parameter)/(higher_parameter-lower_parameter)
    red = (higher_colour[0] - lower_colour[0])
    blue = (higher_colour[2] - lower_colour[2])
    
    return np.array([red, 0, blue])*proportion + lower_colour


def validVelocityFunction(function : str):
    """Checks a string for being a valid velocity function"""
    if re.fullmatch(r" *\d+(\.\d+)?e\^\(i((\*|\/)((-?\d+(\.\d+)?)|-?pi))*\)?", function):
        return True
    return False

