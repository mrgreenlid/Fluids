import pygame
import re
import numpy as np
import numba as nb

# Pygame specifics

def tapping(event : pygame.event.Event):
    """Returns True when a left mouse click is detected, else False"""
    return event.type == pygame.MOUSEBUTTONDOWN
    
def typing(event : pygame.event.Event):
    """Returns True when keystrokes are detected, elese False"""
    return event.type == pygame.KEYDOWN
     

@nb.njit
def pygameToArgand(argand : np.array, pygame_x : int, pygame_y : int):
    """Converts a pygame coordinate to a complex coordinate"""
    return argand[pygame_y, pygame_x]
    

# General algorithms

valid_angle_rule = re.compile(r"((-?\d+(\.\d+)?)|-?[πe])([\*\/]((-?\d+(\.\d+)?)|-?[πe]))*")
def validExpression(rule : re.Pattern, expression : str):
    return bool(rule.fullmatch(expression))

def refineRawArgument(raw_argument : str):
    """Returns the value of a raw argument"""
    angle = re.split(r"([\*\/\-\+])", raw_argument)
    angle = [term for term in angle if term != ""]

    for term in range(len(angle)):
        if angle[term] == "π":
            angle[term] = str(np.pi)
        elif angle[term] == "e":
            angle[term] = str(np.e)
    angle = eval("".join(angle))
    arg = (angle + np.pi) % (2*np.pi) - np.pi

    if arg == -np.pi:
        arg = np.pi

    return arg

@nb.njit
def rgbToInt(colour):
    """Converts an rgb value to an int"""
    return colour[0] * 256 * 256 + colour[1] * 256 + colour[2]


@nb.njit
def mapUniformFlow(magnitude : float, argument : float, width : int, height : int):
    """Maps a uniform velocity function to a complex velocity array"""
    real = magnitude*np.cos(argument)
    imag = magnitude*np.sin(argument)
    return np.full((height, width), real + imag*1j, dtype=np.complex64)


def mapNonUniformFlow(velocity_fuction : str, argand : np.array):
    return argand

    

@nb.njit
def fillScreen(quota : int,  width : int, height : int, pygame_particle_colour : int, pygame_bg_colour):
    """Randomly places particles on a screen"""
    particle_positions = np.full((quota, 2), -1, dtype=np.float64)
    pixel_array = np.full((width, height), pygame_bg_colour)
    
    for particle in range(quota):
        x, y = np.random.randint(0, width-1), np.random.randint(0, height-1)
        if pixel_array[x, y] == pygame_particle_colour:
            continue
        pixel_array[x, y] = pygame_particle_colour
        particle_positions[particle, 0] = x
        particle_positions[particle, 1] = y
        
    return pixel_array, particle_positions


@nb.njit
def mapParticles(pixel_array : np.array, particle_positions : np.array, velocity_array : np.array, dt : float, particle_count : int, particle_colour : int, bg_colour):
    """Maps pixels to a pygame screen array, after movement"""
    width, height = pixel_array.shape[0]-1, pixel_array.shape[1]-1
    # STOP TRAILS
    for particle in range(particle_positions.shape[0]):
        initial_x = particle_positions[particle, 0] 
        initial_y = particle_positions[particle, 1]
        current_index_x = round(initial_x)
        current_index_y = round(initial_y)

        velocity = velocity_array[current_index_y, current_index_x]
        dx, dy = velocity.real*dt, velocity.imag*dt
        dx *= 1 + (np.random.random())
        dy *= 1 + (np.random.random())
        particle_positions[particle, 0] += dx
        particle_positions[particle, 1] -= dy

        x = particle_positions[particle, 0]
        y = particle_positions[particle, 1]

        if not (0 <= x <= width and 0 <= y <= height):
            if x < 0:
                particle_positions[particle, 0] = width
            elif x >= width:
                particle_positions[particle, 0] = 0 

            if y < 0:
                particle_positions[particle, 1] = height
            elif y >= height:
                particle_positions[particle, 1] = 0

            pixel_array[current_index_x, current_index_y] = bg_colour    
            continue
        
        new_index_x = current_index_x
        new_index_y = current_index_y

        if not (current_index_x-1 < x < current_index_x+1):
            new_index_x = round(x)
        
        if not (current_index_y-1 < y < current_index_y+1):
            new_index_y = round(y)
        
        if pixel_array[new_index_x, new_index_y] == particle_colour:
            particle_positions[particle, 0] = initial_x
            particle_positions[particle, 1] = initial_y
            pixel_array[current_index_x, current_index_y] = bg_colour
            continue

        pixel_array[new_index_x, new_index_y] = particle_colour
        pixel_array[current_index_x, current_index_y] = bg_colour
        
    return pixel_array, particle_positions    