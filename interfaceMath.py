import pygame
import re
import numpy as np

ANGLE_PATTERN = re.compile(r"(-?\d+(\.\d+)?)?[πe]*([\*\/\+](-?\d+(\.\d+)?)?[πe]*)*")

def tapping(event : pygame.event.Event):
    """Returns True when a left mouse click is detected, else False"""
    return event.type == pygame.MOUSEBUTTONDOWN
    
def typing(event : pygame.event.Event):
    """Returns True when keystrokes are detected, elese False"""
    return event.type == pygame.KEYDOWN

def validExpression(pattern : re.Pattern, expression):
    """Checks a string against a rule pattern for a full match"""
    return bool(pattern.fullmatch(expression))

def naturaliseArgument(angle : str):
    """Returns a complex argument from a given anticlockwise angle of rotation"""
    angle = re.split(r"([\*\/\-\+πe])", angle)
    angle = [term for term in angle if term != ""]

    for term in range(len(angle)):
        if angle[term] == "π":
            angle[term] = np.pi
        elif angle[term] == "e":
            angle[term] = np.e
        elif angle[term] not in "*/+":
            angle[term] = float(angle[term])

    argument = [angle[0]]
    angle = angle[1:]
    for term in range(len(angle)):
        if type(argument[-1]) == float and type(angle[term]) == float:
            argument[-1] = argument[-1] * angle[term]
        else:
            argument.append(angle[term])

    argument = [str(term) for term in argument]
    argument = eval("".join(argument))
    argument = (argument + np.pi) % (2*np.pi) - np.pi
    if argument == -np.pi:
        argument = np.pi
    return argument

def naturaliseFlowFunction(function : str):
    """Returns a computationally sound velocity function and positions of the general complex terms"""
    function = list(function)
    abs_end = False
    for term in range(len(function)):
        if function[term] == "i":
            function[term] = "1j"
        elif function[term] == "|":
            if abs_end:
                function[term] = ")"
                abs_end = False
            else:
                function[term] = "abs("
                abs_end = True
    function = "".join(function)
    z_positions = []
    for term in range(len(function)):
        if function[term] == "z":
            z_positions.append(term)
    return list(function), z_positions
    
        
