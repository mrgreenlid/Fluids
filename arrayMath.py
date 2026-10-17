import numpy as np
import numba as nb

class Stack:
    def __init__(self):
        self.__stack = []
    
    def push(self):
        ...
    
    def pop(self):
        ...

    def normalise(self):
        ...

    def evaluate(self):
        ...


@nb.njit
def mapFilledScreen(particle_positions : np.array, particle_count : int):
    """Randomly sets postions of fresh set of particles"""
    width = particle_positions.shape[0]
    height = particle_positions.shape[1]
    positions = np.full((width, height, 2), -1, dtype=np.float64)
    quota = particle_count
    if quota >= width*height:
        quota = (width*height)//2
    while quota != 0:
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        if positions[x, y, 0] == -1:
            positions[x, y, 0] = x
            positions[x, y, 1] = y
            quota -= 1   
    return positions

@nb.njit
def pixelArray(particle_positions : np.array, plane : np.array, particle_colour : int):
    """Returns an array of particle positions"""
    pixel_array = plane.copy()
    for x in range(particle_positions.shape[0]-1):
        for y in range(particle_positions.shape[1]-1):
            if particle_positions[x, y, 0] != -1:
                
                pixel_array[x, y] = particle_colour
    return pixel_array

@nb.njit
def mapUniformVelocity(magnitude : float, argument : float, plane_width : int, plane_height : int):
    """Returns a velocity array for a uniform flow"""
    real = magnitude*np.cos(argument)
    imaginary = magnitude*np.sin(argument) * 1j
    return np.full((plane_width, plane_height), real + imaginary, dtype=np.complex64)

def mapNonUniformVelocity(function : str, z_positions, argand : np.array, displacement_scalar : int):
    width = argand.shape[0]
    height = argand.shape[1]
    velocities = np.empty((width, height), dtype=np.complex64)
    for x in range(width-1):
        for y in range(height-1):
            z = argand[x, y]
            for pos in z_positions:
                function[pos] = str(z)
            try:
                velocities[x, y] = eval("".join(function))*displacement_scalar
            except ZeroDivisionError:
                velocities[x, y] = 0j
    return velocities

@nb.njit
def moveParticles(particle_positions : np.array, velocities : np.array, dt : float, uniform : bool = True):
    """Updates particle positions by their point velocity"""
    width = particle_positions.shape[0]-1
    height = particle_positions.shape[1]-1
    
    particles = np.argwhere(particle_positions[:, :, 0] != -1)
    
    for position in particles:
        x = position[0]
        y = position[1]

        velocity = velocities[x, y]
        dx = velocity.real*(1 + np.random.random())*dt*10
        dy = velocity.imag*(1 + np.random.random())*dt*10

        potential_x = x + dx
        potential_y = y - dy

        if not (0 <= potential_x <= width and 0 <= potential_y <= height):
            if uniform: 
                potential_x %= width
                potential_y %= height

            else:
                potential_x = np.random.randint(0, width)
                potential_y = np.random.randint(0, height)
                
                    
        new_x = round(potential_x)
        new_y = round(potential_y)

        if particle_positions[new_x, new_y, 0] != -1:
            continue
        
        particle_positions[x, y, 0] = -1
        particle_positions[x, y, 1] = -1
        particle_positions[new_x, new_y, 0] = potential_x
        particle_positions[new_x, new_y, 1] = potential_y


    return particle_positions




