import pygame

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
