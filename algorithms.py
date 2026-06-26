import pygame
import numpy as np

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


    