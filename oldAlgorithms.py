import pygame
import sqlite3 as sqlite
from typing import Tuple
import re
import numpy as np
import numba as nb



#### Need to sort out the origin location of a particle before instantiating

class Output:
    class_type = "output"

class Input:
    class_type = "input"


# Pygame specific subroutines
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


# General, mathematical subroutines
def toggleVariable(var : bool):
    """Returns the opposite value to the one passed in"""
    return not var

@nb.njit
def kineticEnergy(mass : float, speed : float):
    return 0.5*mass*speed*speed

@nb.njit
def rotate(point : np.array, radians : float):
    """Rotates np.array group of coordinates about the origin"""
    radians *= -1
    
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)],
                                [np.sin(radians), np.cos(radians)]], dtype=np.float64)
    
    return point @ rotation_matrix.T

@nb.njit
def translate(point: np.array, pygame_x : int, pygame_y : int):
    """Translates np.array group of coordinates"""
    point = np.copy(point)
    for dot in range(point.shape[0]):
        point[dot][0] += pygame_x
        point[dot][1] += pygame_y
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

@nb.njit
def addVariation(minimum : float, maximum : float):
    return np.random.choice(np.linspace(minimum, maximum))

@nb.njit
def mapVelocities(exponential : int, magnitude : float, argument : float, height : int, width : int , speed : float):
    """Updates a velocities array for each point"""
    velocities = np.ones((height, width), dtype=np.complex128)
    if exponential == 1:
        velocities = np.ones((height, width), dtype=np.complex128)
        complex_point = magnitude*np.cos(argument) + 1j*magnitude*np.sin(argument)
        velocities *= complex_point*speed
    else:
        velocities = np.zeros((height,width), dtype=np.complex128)
    return velocities

       


# Database subroutines
def initialiseVelocityFunctionTable():
    """Creates table in fluids database to store velocity functions and sets up prebuilt functions"""
    with sqlite.Connection("fluids.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS velocity_function (
                    written TEXT UNIQUE,
                    exponential INTEGER,
                    magnitude TEXT,
                    argument TEXT);

                    INSERT or IGNORE INTO velocity_function VALUES ("tunnel", 1, "1", "pi");
                    INSERT or IGNORE INTO velocity_function VALUES ("vortex", 1, "1", "pi*-0.25");
                    INSERT or IGNORE INTO velocity_function VALUES ("falling", 1, "1", "pi*0.5");

                    """)
        conn.commit()


def getVelocityFunction(function : str):
    """Searches the velocity function table, written attribute, for the criteria"""
    with sqlite.Connection("fluids.db") as conn:
        function_data = conn.cursor().execute("""SELECT * FROM velocity_function WHERE written = (?) """, (function,)).fetchone()
        conn.commit()
    return function_data

def validVelocityFunction(function : str):
    """Checks if a string is formatted correctly to be a velocity function"""
    if re.fullmatch(r"\d+(\.\d+)?e\^\(i(\*(\d+(\.\d+)?|pi))*\)", function):
        return True
    else:
        return False

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



def initialiseBodyTable():
    """Creates table in fluids database to store body names, their properties and associated image paths"""
    with sqlite.Connection("fluids.db") as conn:
        conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS body
        (num INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        path TEXT,
        fixed INTEGER,
        mass REAL,
        display_scale_factor REAL);
        
        INSERT or IGNORE INTO body VALUES (1, "circle", "images\\body\\circle.png", 0, 10.0, 0.7);
        INSERT or IGNORE INTO body VALUES (2, "square", "images\\body\\square.png", 0, 10.0, 0.8);
        INSERT or IGNORE INTO body VALUES (3, "airfoil", "images\\body\\airfoil.png", 1, 0.0, 0.9);
        INSERT or IGNORE INTO body VALUES (4, "f1 car", "images\\body\\car.png", 1, 0.0, 0.7);""")
        conn.commit()
        

def getBodyProperties(index : int):
    """Returns the properties of an object of a given index"""
    with sqlite.Connection("fluids.db") as conn:
        return conn.cursor().execute("""SELECT * FROM body WHERE num = ?""", (index,)).fetchone()[1:]


