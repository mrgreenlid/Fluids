import pygame
import cmath
import math
import sqlite3 as sqlite
import re

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

def arg(z : complex):
    """Returns the argument [-pi, pi] of a complex number"""
    return cmath.phase(z)

def magnitude(z : complex):
    """Returns the magnitude of a complex number"""
    return math.sqrt(z.real**2 + z.imag**2)

def kineticEnergy(speed : int | float, mass : int | float):
    """Returns the kinetic energy of an object of given speed and mass"""
    return 0.5*mass*(speed**2)

def searchVelocityFunction(function : str):
    """Searches the velocity function table, written attribute, for the criteria"""
    with sqlite.Connection("fluids.db") as conn:
        function_data = conn.cursor().execute("""SELECT * FROM velocity_function WHERE written = (?) """, (function,)).fetchone()
        conn.commit()
    return function_data

def validVelocityFunction(function : str):
    """Checks if a string is formatted correctly to be a velocity function"""
    if re.fullmatch(r"\d+(\.\d+)?e\^\(i(\*(\d+(\.\d+)?|pi))+\)", function):
        return True

def saveVelocityFunction():
    """Adds a new velocity function to the table"""
    ...


