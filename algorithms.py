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
def mapUniformFlow(magnitude : float, argument : float, argand : np.array):
    """Maps a uniform velocity function to a complex velocity array"""
    width = argand.shape[0]
    height = argand.shape[1]
    real = magnitude*np.cos(argument)
    imag = magnitude*np.sin(argument)
    return np.full((width, height), real + imag*1j, dtype=np.complex64)

def naturaliseVelocityFunction(velocity_function : str):
    z_positions = []
    end_mod = False
    velocity_function = list(velocity_function)
    for char in range(len(velocity_function)):
        if velocity_function[char] == "i":
            velocity_function[char] = str(1j)
        elif velocity_function[char] == "|":
            if not end_mod:
                velocity_function[char] = "abs("
                end_mod = True
            else:
                velocity_function[char] = ")"
                end_mod = False
    for char in range(len(velocity_function)):
        if velocity_function[char] == "z":
            z_positions.append(char)
    return velocity_function, z_positions
  
def mapNonUniformFlow(velocity_function : str, argand : np.array, clockScalar):
    width = argand.shape[0]
    height = argand.shape[1]
    velocities = np.empty((width, height), dtype=np.complex64)
    velocity_function, z_positions = naturaliseVelocityFunction(velocity_function)
    for y in range(argand.shape[1]-1):
        for x in range(argand.shape[0]-1):
            z = argand[x, y]
            for pos in z_positions:
                velocity_function[pos] = str(z)
            try:
                velocities[x, y] = eval("".join(velocity_function))*clockScalar
                # np.Vectorise instead?
            except ZeroDivisionError:
                velocities[x, y] = 0j
    return velocities

@nb.njit
def mapFilledScreen(quota : int, particle_positions : np.array, particle_colour : int, bg_colour : int):
    """Randomly sets positions of particles"""
    width = particle_positions.shape[0]
    height =  particle_positions.shape[1]
    particle_positions = np.full((width, height, 2), -1, dtype=np.float64)
    for particle in range(quota):
        x = np.random.randint(0, width-1)
        y = np.random.randint(0, height-1)
        if particle_positions[x, y, 0] == -1:
            particle_positions[x, y, 0] = x
            particle_positions[x, y, 1] = y
    return particle_positions

@nb.njit
def mapParticles(particle_positions : np.array, velocity_array : np.array, dt : float, uniform : bool = True, non_uniform_source = (-1, -1)):
    max_x = particle_positions.shape[0]-1
    max_y = particle_positions.shape[1]-1
    particles = np.argwhere(particle_positions[:, :, 0] != -1)
    
    for particle in particles:
        current_index_x = new_index_x = particle[0]
        current_index_y = new_index_y = particle[1]
        initial_x = particle_positions[current_index_x, current_index_y, 0]
        initial_y = particle_positions[current_index_x, current_index_y, 1]
    
        velocity = velocity_array[current_index_x, current_index_y]
        dx = velocity.real*(1 + np.random.random())*dt
        dy = velocity.imag*(1 + np.random.random())*dt
        potential_x = initial_x + dx
        potential_y = initial_y + dy

        
        if not (0 <= potential_x <= max_x and 0 <= potential_y <= max_y):
            if uniform: 
                if potential_x < 0:
                    potential_x = max_x
                elif potential_x > max_x:
                    potential_x = 0

                if potential_y < 0:
                    potential_y = max_y
                elif potential_y > max_y:
                    potential_y = 0
            else:
                if non_uniform_source[0] == -1:
                    potential_x = np.random.randint(0, max_x)
                else:
                    potential_x = non_uniform_source[0]
                
                if non_uniform_source[1] == -1:
                    potential_y = np.random.randint(0, max_y)
                else:
                    potential_y = non_uniform_source[1]
            


        if not (current_index_x-1 < potential_x < current_index_x+1):
            new_index_x = round(potential_x)
        
        if not (current_index_y-1 < potential_y < current_index_y+1):
            new_index_y = round(potential_y)
        
        if particle_positions[new_index_x, new_index_y, 0] != -1:
            continue

        particle_positions[current_index_x, current_index_y, 0] = -1
        particle_positions[current_index_x, current_index_y, 1] = -1
        particle_positions[new_index_x, new_index_y, 0] = potential_x
        particle_positions[new_index_x, new_index_y, 1] = potential_y

    return particle_positions

@nb.njit  
def makePixelArray(particle_positions : np.array, plane : np.array, particle_colour : int):
    particles = np.argwhere(particle_positions[:, :, 0] != -1)
    pixel_array = plane.copy()
    for particle in particles:
        x = particle[0]
        y = particle[1]
        if pixel_array[x, y] != particle_colour:
            pixel_array[x, y] = particle_colour

    return pixel_array

