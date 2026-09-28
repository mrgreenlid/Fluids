import pygame
import re
import numpy as np
import numba as nb

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
def pygameToArgand(argand : np.array, x : int, y : int):
    """Converts a pygame coordinate to a complex coordinate"""
    return argand[y][x]
    
# General algorithms
def validAngleExpression(expression : str):
    return bool(re.fullmatch(r"((-?\d+(\.\d+)?)|-?[πe])([\*\/]((-?\d+(\.\d+)?)|-?[πe]))*", expression))

@nb.njit
def rgbToInt(colour):
    """Converts an rgb value to an int"""
    return colour[0] * 256 * 256 + colour[1] * 256 + colour[2]

def refineRawArgument(raw_angle : str):
    """Returns the value of a raw, angle string"""
    angle = re.split(r"([\*\/\-])", raw_angle)
    angle = [term for term in angle if term != ""]
    negative_flag = False
    
    for term in range(len(angle)):
        if angle[term] == "π":
            angle[term] = str(np.pi)
        elif angle[term] == "e":
            angle[term] = str(np.e)
        elif angle[term] == "-":
            negative_flag = True
            continue
        if negative_flag:
            angle[term] = str(float(angle[term])*-1)
            negative_flag = False
    angle = [term for term in angle if term != "-"]
    angle = eval("".join(angle)) 

    negative = False
    if angle < 0:
        negative = True
    angle = (angle + np.pi) % (2*np.pi) - np.pi
    if abs(angle) == np.pi :
        angle = np.pi
    return angle
        
@nb.njit
def mapUniformFlow(argand : np.array, magnitude : float, theta : float):
    """Maps a uniform flow function to a velocity field array"""
    real_component = magnitude*np.cos(theta)
    imag_component = magnitude*np.sin(theta)
    return np.full((argand.shape[0], argand.shape[1]), real_component + imag_component*1j, dtype=np.complex64)



def mapNonUniformFlow(velocity_function : str):
    """Maps a non uniform flow function to a velocity field array"""
    ...


@nb.njit
def selectSource(sources : np.array, source_variance : int, max_width : int, max_height : int):
    """Selects a source location for a particle"""
    variance = np.random.randint(-source_variance, source_variance)
    x, y = sources[np.random.randint(0, sources.shape[0])]
    if x == 0 or x == max_width:
        y += variance
    elif y == 0 or y == max_height:
        x += variance
    return x, y
    

@nb.njit
def mapParticles(pixel_array : np.array, particle_positions : np.array, precise_particle_positions : np.array, velocity_array : np.array, sources : np.array, source_variance : int, dt : float, particle_count : int, pygame_particle_colour : int, pygame_bg_colour : int):
    """Maps particles onto a pixel array"""
    empty = np.array([-1, -1])
    on_screen = (particle_positions != empty).sum()
    width, height = pixel_array.shape[0]-1, pixel_array.shape[1]-1


    for particle in range(particle_count - on_screen):
        x, y = selectSource(sources, source_variance, width, height)
        if pixel_array[x, y] == pygame_particle_colour:
            continue
        new_coords = np.array([x, y])
        next_free = np.argmin(particle_positions) // 2
        pixel_array[x, y] = pygame_particle_colour
        particle_positions[next_free] = new_coords
        precise_particle_positions[next_free] = new_coords
 
    
    for particle in range(particle_positions.shape[0]):
        x = particle_positions[particle, 0]
        y = particle_positions[particle, 1]
        velocity = velocity_array[y, x]
        dx, dy = velocity.real*dt, velocity.imag*dt
        precise_particle_positions[particle, 0] += dx
        precise_particle_positions[particle, 1] += dy

        exact_x = precise_particle_positions[particle, 0]
        exact_y = precise_particle_positions[particle, 1]

        if not (0 <= exact_x <= width and 0 <= exact_y <= height):
            pixel_array[x, y] = pygame_bg_colour
            particle_positions[particle, 0] = -1
            particle_positions[particle, 1] = -1
            precise_particle_positions[particle, 0] = -1
            precise_particle_positions[particle, 1] = -1
            continue
        
        new_x, new_y = x, y

        if not (x-1 < exact_x < x+1):
            new_x = int(np.rint(exact_x))
        
        if not (y-1 < exact_y < y+1):
            new_y = int(np.rint(exact_y))
        
        if pixel_array[new_x, new_y] == pygame_particle_colour:
            # Add collisions here?
            continue

        pixel_array[new_x, new_y] = pygame_particle_colour
        pixel_array[x, y] = pygame_bg_colour
        particle_positions[particle, 0] = new_x
        particle_positions[particle, 1] = new_y
    


    return pixel_array, particle_positions, precise_particle_positions
    
