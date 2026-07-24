import pygame
import cmath
import math
import sqlite3 as sqlite
from typing import Tuple
import re
import numpy as np
import numba as nb

# Basic subroutines for interface components 
class Output:
    class_type = "output"

class Input:
    class_type = "input"

def tapping(event : pygame.event.Event):
    """Checks for tapping"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    return False

def typing(event : pygame.event.Event):
    """Checks for typing"""
    if event.type == pygame.KEYDOWN:
        return True
    return False

def toggleVariable(var : bool):
    """Returns the opposite value to the one passed in"""
    return not var

def kineticEnergy(speed : int | float, mass : int | float):
    """Returns the kinetic energy of an object of given speed and mass"""
    return 0.5*mass*(speed**2)

@nb.njit
def rotate(point : np.array, radians : float):
    """Rotates a tuple coordinate, or np.array group of coordinates about the origin"""
    radians *= -1
    
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                [np.sin(radians), np.cos(radians)]])

    if point.ndim == 1:
        return rotation_matrix @ point
    else:
        return point @ rotation_matrix.T
        

def translate(point: np.array, pygame_x : int, pygame_y : int):
    """Translates a tuple coordinate, or np.array group of coordinates"""
    point += [pygame_x, pygame_y]
    return point



def searchVelocityFunction(function : str):
    """Searches the velocity function table, written attribute, for the criteria"""
    with sqlite.Connection("fluids.db") as conn:
        function_data = conn.cursor().execute("""SELECT * FROM velocity_function WHERE written = (?) """, (function,)).fetchone()
        conn.commit()
    return function_data

def validVelocityFunction(function : str):
    """Checks if a string is formatted correctly to be a velocity function"""
    if re.fullmatch(r"\d+(\.\d+)?e\^\(i(\*(\d+(\.\d+)?|pi))*\)", function):
        return True

def saveVelocityFunction(function : str):
    """Adds a new velocity function to the table"""
    # May remove selection if not adding general formula adding
    if "e" in function:
        magnitude = function[:function.index("e")]
        if "*" in function:
            argument = function[function.index("*")+1:function.index(")")]
        else:
            argument = 0
        with sqlite.Connection("fluids.db") as conn:
            conn.cursor().execute("""INSERT or IGNORE INTO velocity_function VALUES (?,?,?,?)""",
            (function, 1, magnitude, argument))


