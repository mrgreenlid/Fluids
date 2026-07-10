import pygame
import cmath
import sqlite3 as sqlite



# Creates table in fluids database to store velocity functions
with sqlite.Connection("fluids.db") as conn:
    conn.cursor().execute("""CREATE TABLE IF NOT EXISTS function (
                written TEXT PRIMARY KEY,
                exponential INTEGER,
                magnitude TEXT,
                argument TEXT)
                """)


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
    return cmath.sqrt(z.real**2 + z.imag**2)

def kineticEnergy(speed : int | float, mass : int | float):
    """Returns the kinetic energy of an object of given speed and mass"""
    return 0.5*mass*(speed**2)