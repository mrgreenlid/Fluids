import pygame
from algorithms import *
from typing import Tuple, List


class Box:
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, width : int, height : int, colour : str):
        """Creates box to be placed on screen"""
        self.__window = window
        self.__colour = colour
        self.__rect = pygame.Rect(0, 0, width, height)
        self.__rect.center = (x,y)

    def place(self):
        """Draws box at preset location"""
        pygame.draw.rect(self.__window, self.__colour, self.__rect)
        pygame.draw.rect(self.__window, "#000000", self.__rect, 1)


class Label:
    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, size : int, bg : str, font : str = "Consolas"):
        """Creates text label to be placed on screen"""
        self._window = window
        self._size = size
        self._bg = bg
        self._text = f"{text}"

        # Creates a set of arguments to be used to render the text
        self._render_arguments = [self._text, True, "black", self._bg]

        # Creates the font object, rect and sets position
        self._font = pygame.font.SysFont(font, self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x,y)

    def place(self):
        """Places label at preset location"""
        self._window.blit(self._font.render(*self._render_arguments), self._rect)


class Entry(Label, Input):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"

    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, variable : str, datatype : type, size : int = 25):
        """Creates entry box to be placed on screen"""
        super().__init__(window, x, y, " ", size, self._inactive_colour, "Courier")

        self._text = f"{text}"
        self._variable = variable
        self._datatype = datatype
        self._in_use = False

        # Lengthens the box 
        self._rect.width = 120
        self._updateText()

    def place(self):
        """Places entry box at preset location"""
        pygame.draw.rect(self._window, self._bg, self._rect)
        super().place()
        pygame.draw.rect(self._window, "#000000", self._rect, 1)

    def _click(self):
        """Changes box to active colours"""
        self._bg = self._active_colour
        self._in_use = True
        self._updateText()

    def _antiClick(self):
        """Changes box to inactive colours"""
        self._bg = self._inactive_colour
        self._in_use = False
        self._updateText()

    def __errorCorrect(self):
        """Checks text for syntax and logic errors"""
        if self._datatype == float:
            try:
                if self._text[0] == "0" and self._text[1] != ".":
                    self._text = self._text[1:]
            except IndexError:
                pass

            if len(self._text) == 0 and not self._in_use:
                self._text = "0"

            if len(self._text) > 5 :
                self._text = self._text[:5]

    def _updateText(self):
        """Cements changes to text"""
        self.__errorCorrect()
        self._render_arguments[0], self._render_arguments[3] = self._text, self._bg

    def _typeText(self, event):
        """Changes text by keyboard input"""
        key = event.unicode

        if key == "\x08":
            self._text = self._text[:-1]

        elif key == "\x0D":
            self._updateText()
            self._antiClick()

        if self._datatype == float:
            if key.isdigit() or (key == "." and "." not in self._text):
                self._text += key

        self._updateText()

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                self._click()

            else:
                self._updateText()
                self._antiClick()

        if self._in_use:
            if typing(event):
                self._typeText(event)

    def getVariable(self):
        """Returns associated variable"""
        return self._variable

    def getValue(self):
        """Returns value"""
        if self._datatype == float:
            return float(self._text)
        elif self._datatype == str:
            return self._text.lower()
        return None

class Dropdown(Entry, Input):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, options : Tuple[str], variable : str, datatype : type):
        """Creates dropdown box to be placed on screen"""
        super().__init__(window, x, y, options[0], variable, datatype)

        self.__options = options
        self.__option_rect = [self._rect.copy() for _ in range(len(self.__options))]
        for rect in range(len(self.__options)):
            self.__option_rect[rect].centery += (30*(rect+1))

        # Creates rect and coords for dropdown button
        self.__arrow_rect = pygame.Rect(0, 0, 30, 30)
        self.__arrow_rect.center = (x + 140, y + 1)
        self.__arrow_coordinates = [(self.__arrow_rect.centerx, self.__arrow_rect.centery + 2.5),
                                    (self.__arrow_rect.centerx + 5, self.__arrow_rect.centery - 2.5),
                                    (self.__arrow_rect.centerx - 5, self.__arrow_rect.centery - 2.5)]

    def place(self):
        """Draws main box, button and options"""
        super().place()
        pygame.draw.rect(self._window, "#D3D3D3", self.__arrow_rect)
        pygame.draw.rect(self._window, "#000000", self.__arrow_rect, 1)
        pygame.draw.polygon(self._window, "#000000", self.__arrow_coordinates)

        if self._in_use:
            for rect in range(len(self.__option_rect)):
                pygame.draw.rect(self._window, "#FFFFFF", self.__option_rect[rect], 0)
                self._window.blit(self._font.render(self.__options[rect], True, "#000000", "#FFFFFF"), self.__option_rect[rect])
                pygame.draw.rect(self._window, "#000000", self.__option_rect[rect], 1)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if not self._in_use:
                if self.__arrow_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                    self._click()
            else:
                for rect in range(len(self.__option_rect)):
                    if self.__option_rect[rect].collidepoint(*pygame.mouse.get_pos()[:2]):
                        self._text = self.__options[rect]
                self._antiClick()

        if self._in_use:
            if typing(event):
                if event.unicode == "\x0D":
                    self._antiClick()

class Checkbox(Input):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str):
        """Creates checkbox to be placed on screen"""
        self._window = window
        self._variable = variable
        self._state = False
        self._bg = self._inactive_colour
        self._rect = pygame.Rect(0, 0, 25, 25)
        self._rect.center = (x, y)

    def place(self):
        """Draws checkbox, with border"""
        pygame.draw.rect(self._window, self._bg, self._rect)
        pygame.draw.rect(self._window, "#000000", self._rect, 1)

    def _click(self):
        """Changes box to active colours"""
        self._bg = self._active_colour
        self._state = True

    def _antiClick(self):
        """Changes box to inactive colours"""
        self._bg = self._inactive_colour
        self._state = False

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                if self._state:
                    self._antiClick()
                else:
                    self._click()

    def getVariable(self):
        """Returns associated variable"""
        return self._variable

    def getValue(self):
        """Returns value"""
        return self._state

class DoubleCheckbox(Checkbox):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, x_displacement : int, y_displacement, variable : str):
        """Creates pair of linked checkboxes to be placed on screen"""
        super().__init__(window, x, y, variable)
        self.__rect2 = self._rect.copy()
        self.__rect2.centerx  += x_displacement
        self.__rect2.centery +=  y_displacement
        self.__bg2 = self._inactive_colour
        self._bg = self._active_colour
        self._state = True

    def place(self):
        """Draws checkboxs, with border"""
        super().place()
        pygame.draw.rect(self._window, self.__bg2, self.__rect2)
        pygame.draw.rect(self._window, "#000000", self.__rect2, 1)
    
    def _click(self):
        """Changes appropriate box colours"""
        self._bg = self._active_colour
        self.__bg2 = self._inactive_colour
        self._state = True

    def _antiClick(self):
        """Changes appropriate box colours"""
        self._bg = self._inactive_colour
        self.__bg2 = self._active_colour
        self._state = False

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                self._click()
            elif self.__rect2.collidepoint(*pygame.mouse.get_pos()[:2]):
                self._antiClick()
            
class Button(Input):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str, path_1 : str, path_2 : str = None, scale_factor_1 : Tuple[int] = None, scale_factor_2 : Tuple[int] = None, key_bind : str = None):
        """Creates button to be placed on screen"""
        self.__window = window
        self.__variable = variable

        self.__state = False

        self.__off_shape = pygame.transform.scale_by(pygame.image.load(path_1).convert_alpha(), scale_factor_1)
        self.__off_rect = self.__off_shape.get_rect()
        self.__off_rect.center = (x, y)

        if path_2:
            self.__on_shape = pygame.transform.scale_by(pygame.image.load(path_2).convert_alpha(), scale_factor_2)
            self.__on_rect = self.__on_shape.get_rect()
            self.__on_rect.center = (x, y)

        try:
            self.__key_bind = pygame.key.key_code(key_bind)
        except TypeError:
            self.__key_bind = False

    def place(self):
        """Blits the relevant image"""
        if self.__state:
            self.__window.blit(self.__on_shape, self.__on_rect)
        else:
            self.__window.blit(self.__off_shape, self.__off_rect)

    def checkInteract(self, event : pygame.event.Event, keys : List[bool]):
        """Checks for interactions"""
        if tapping(event):
            if self.__state:
                if self.__on_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                    self.__state = False
            else:
                if self.__off_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                    self.__state = True
        if self.__key_bind:
            if typing(event):
                if keys[self.__key_bind]:
                    self.__state = toggleVariable(self.__state)

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable

    def getValue(self):
        """Returns value"""
        return self.__state


class Increment(Input):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str, minimum : int | float, maximium : int | float, increment : int | float,):
        """Creates increment buttons to be placed on screen"""
        self.__window = window
        self.__variable = variable
        self.__maximum = maximium
        self.__value = self.__minimum = minimum
        self.__increment = increment
        self.__up_rect = pygame.rect.Rect(0,0,25,25)
        self.__down_rect = self.__up_rect.copy()
        self.__up_rect.center = (x+15, y)
        self.__down_rect.center = (x-15, y)

        self.__up_arrow_coordinates = [(self.__up_rect.centerx, self.__up_rect.centery-2.5),
                                        (self.__up_rect.centerx -5, self.__up_rect.centery + 2.5),
                                        (self.__up_rect.centerx +5, self.__up_rect.centery +2.5)]
        
        self.__down_arrow_coordinates = [(self.__down_rect.centerx, self.__down_rect.centery+2.5),
                                        (self.__down_rect.centerx -5, self.__down_rect.centery - 2.5),
                                        (self.__down_rect.centerx +5, self.__down_rect.centery -2.5)]

    def place(self):
        """Draws increment buttons"""
        pygame.draw.rect(self.__window, "#D3D3D3", self.__up_rect)
        pygame.draw.rect(self.__window, "#000000", self.__up_rect, 1)
        pygame.draw.rect(self.__window, "#D3D3D3", self.__down_rect)
        pygame.draw.rect(self.__window, "#000000", self.__down_rect, 1)
        pygame.draw.polygon(self.__window, "#000000", self.__up_arrow_coordinates)
        pygame.draw.polygon(self.__window, "#000000", self.__down_arrow_coordinates)

    def checkInteract(self, event):
        """Checks for interactions"""
        if tapping(event):
        
            if self.__up_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                if (self.__value + self.__increment) <= self.__maximum:
                    self.__value += self.__increment
            elif self.__down_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                if (self.__value - self.__increment) >= self.__minimum:
                    self.__value -= self.__increment
            

    def getVariable(self):
        return self.__variable
    
    def getValue(self):
        return self.__value