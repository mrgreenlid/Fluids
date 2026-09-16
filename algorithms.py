import pygame
import re
import numpy as np

# Pygame specifics
def tapping(event : pygame.event.Event):
    """Returns True when a left mouse click is detected, else False"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    return False

def typing(event : pygame.event.Event):
    """Returns True when keystrokes are detected, elese False"""
    if event.type == pygame.KEYDOWN:
        return True
    else:
        False

@nb.njit
def drawParticles(pixels : np.array, velocities : np.array):
    """Maps particles on a plane, moved by the complex point velocity"""
    ...
    


# General algorithms
def validExpression(expression : str):
    if re.fullmatch(r"\s*(-?\d+(?:\.\d+)?|-?π|-?e)(?:\s*(?:\*|/)\s*(-?\d+(?:\.\d+)?|-?π|-?e))*\s*", expression):
        return True
    return False

def rawAngleRefine(angle : str):
    """Returns the value of a raw, angle string"""
    value = 1
    terms = [term for term in re.split(r"(π|e|\*|/|-)", angle) if term != ""]
    refined = []
    for term in range(len(terms)):
            if terms[term] == "π":
                refined.append(str(np.pi))
            elif terms[term] == "e":
                refined.append(str(np.e))
            else:
                refined.append(terms[term])
    refined = "".join(refined)
    return eval(refined)

def mapUniformFlow(argand : np.array, magnitude : float, theta : float):
    """Maps a uniform flow function to a velocity field array"""
    real_component = magnitude*np.cos(theta)
    imag_component = magnitude*np.sin(theta)
    return np.full((argand.shape[0], argand.shape[1]), real_component + imag_component*1j, dtype=np.complex64)
    