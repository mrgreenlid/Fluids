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
    """Rotates np.array group of coordinates about the origin"""
    radians *= -1
    point = point.astype(np.float64)
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                [np.sin(radians), np.cos(radians)]], dtype=np.float64)
                                
    return point @ rotation_matrix.T

@nb.njit
def translate(point: np.array, pygame_x : int, pygame_y : int):
    """Translates np.array group of coordinates"""
    point = point.astype(np.float64)
    for dot in range(point.shape[0]):
        point[dot][0] += pygame_x
        point[dot][1] += pygame_y
    return point

##### Is the checker in vector field too inefficiet?
@nb.njit
def colourByMagnitude(magnitude: float):
    """Returns an RGB value for a temperature colour based on a given magnitude"""
    value = round(magnitude)

    colours = np.array([(0,0,255),(10,0,245),(20,0,235),(31,0,224),(41,0,214),(51,0,204),
    (61,0,194),(71,0,184),(82,0,173),(92,0,163),(102,0,153),(112,0,143),(122,0,133),
    (133,0,122),(143,0,112),(153,0,102),(163,0,92),(173,0,82),(184,0,71),(194,0,61),
    (204,0,51),(214,0,41),(224,0,31),(235,0,20),(255,0,0)], dtype=np.float64)
        
    parameters = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120], dtype=np.float64)

    place_check = np.sort(np.append(parameters, value))
    position = np.where(place_check == value)[0][0]

    if position == 0 or value in parameters:
        return colours[position]
    elif value == place_check[-1]:
        return colours[-1]
    
    proportion = (value-parameters[position-1])/(parameters[position]-parameters[position-1])
    addition = np.array([colours[position][0]-colours[position-1][0], 0, colours[position][2]-colours[position-1][2]])*proportion
    return colours[position-1]+addition



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


