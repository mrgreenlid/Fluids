import pygame
from algorithms import *
import re
from typing import Tuple

class Box:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int, colour : str = "#000000", outline : bool = False):
        """A pygame box"""
        self.__screen = screen
        self.__colour = colour
        self.__outline = outline
        self.__rect = pygame.Rect(0, 0, width, height)
        self.__rect.center = (x, y)

    def place(self):
        """Places the box on the screen"""
        pygame.draw.rect(self.__screen, self.__colour, self.__rect)
        if self.__outline:
            pygame.draw.rect(self.__screen, "#000000", self.__rect, 1)

class Label:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, text : str = "", size : int = 20, colour : str = "#000000", bg : str = "#FFFFFF", font : str = "Segoe UI"):
        """A pygame label"""
        self._screen = screen
        self._size = size
        self._colour = colour
        self._bg = bg

        self._render_arguments = [f"{text}", True, self._colour, self._bg]

        self._font = pygame.font.SysFont(font, self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x, y)
    
    def place(self):
        """Places the label on the screen"""
        self._screen.blit(self._font.render(*self._render_arguments), self._rect)

class DataLabel(Label):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str, text : str = "", size : int = 20, colour : str = "#000000", bg : str = "#FFFFFF", dtype : type = float, font : str = "Segoe UI"):
        """A pygame data label"""
        super().__init__(screen, x, y, " ", size, colour, bg, font)
        self._render_arguments[0] = f"{text}"
        self.__identifier = identifier
        self.__dtype = dtype
    
    def update(self, updated_text : str):
        """Updates the text displayed"""
        if self.__dtype == float or self.__dtype == int:
            self._render_arguments[0] = f"{updated_text:.{10}f}"[:7]
        else:
            self._render_arguments[0] = updated_text
        
    def getIdentifier(self):
        """Returns the identifier for the data"""
        return self.__identifier

class Entry(Label):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str,  text : str = "", size : int = 25,  max_length : int = 10, width : int = 150, dtype : type = float, font : str = "Segoe UI"):
        """A pygame entry box"""
        super().__init__(screen, x, y, " ", size, "#000000", self._inactive_colour, font)
        self._text = f"{text}"
        self._max_length = max_length
        self._rect.width = width
        self._identifier = identifier
        self._dtype = dtype
        self._state = False
        self._bg = self._inactive_colour

        self._updateText()

    def place(self):
        """Places the entry box on the screen"""
        pygame.draw.rect(self._screen, self._bg, self._rect)
        super().place()
        pygame.draw.rect(self._screen, "#000000", self._rect, 1)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                self._click()
            else:
                self._antiClick()
        
        if self._state:
            if typing(event):
                key = event.unicode
                if key == "\x08":
                    self._text = self._text[:-1]
                elif key == "\x0D":
                        self._antiClick()
                elif (self._dtype == float and (key.isdigit() or (key == "." and "." not in self._text))) or self._dtype == str:
                    self._text += key
                self._updateText()

    def _updateText(self):
        """Updates attributes of the text"""
        if self._dtype == float:
            if not self._state:
                if len(self._text) == 0:
                    self._text = "0"

            if re.match(r"^0+[0-9]", self._text):
                self._text = self._text[1:]

        if len(self._text) > self._max_length:
            self._text = self._text[:-1]
        
        self._render_arguments[0] = self._text
        self._render_arguments[3] = self._bg
              
    def _click(self):
        """Updates the box to show a click on"""
        self._bg = self._active_colour
        self._state = True
        self._updateText()
    
    def _antiClick(self):
        """Updates the box to show a click off"""
        self._bg = self._inactive_colour
        self._state = False
        self._updateText()

    def addText(self, character : str):
        if character == "back":
            self._text = self._text[:-1]
        elif character == "return":
            self._antiClick()
        else:
            self._text += character


    def getIdentifier(self):
        """Returns the associated identifier"""
        return self._identifier

    def getValue(self):
        """Returns value"""
        if self._dtype == float:
            try:
                return float(self._text)
            except ValueError:
                return 0.0
        elif self._dtype == str:
            return self._text.lower()
        return None

class Dropdown(Entry):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str, options : Tuple[str] | Tuple[int], size : int = 25, width : int = 150, dtype : type = float, font : str = "Segoe UI"):
        """A pygame dropdown box"""
        super().__init__(screen, x, y, identifier, options[0], size, len(sorted(list(options), key=len)[-1]), width, dtype, font)
        self.__options = options
        self.__options_rect = []
        self.__current_options = []

        for option in range(len(self.__options)-1):
            option_rect = self._rect.copy()
            option_rect.centery += 30*(option+1)
            self.__options_rect.append(option_rect)
        
        self.__arrow_rect = pygame.Rect(x+width, y-15, 30, 30)
        self.__arrow_coordinates = [(self.__arrow_rect.centerx, self.__arrow_rect.centery + 2.5),
                                    (self.__arrow_rect.centerx + 5, self.__arrow_rect.centery - 2.5),
                                    (self.__arrow_rect.centerx - 5, self.__arrow_rect.centery - 2.5)]

    def place(self):
        """Places the dropdown box on the screen"""
        super().place()
        pygame.draw.rect(self._screen, "#D3D3D3", self.__arrow_rect)
        pygame.draw.rect(self._screen, "#000000", self.__arrow_rect, 1)
        pygame.draw.polygon(self._screen, "#000000", self.__arrow_coordinates)
        
        if self._state:
            for option in range(len(self.__current_options)):
                pygame.draw.rect(self._screen, "#FFFFFF", self.__options_rect[option])
                self._screen.blit(self._font.render(self.__current_options[option], True, "#000000", "#FFFFFF"), self.__options_rect[option])
                pygame.draw.rect(self._screen, "#000000", self.__options_rect[option], 1)
    
    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if not self._state:
                self.__configureOptions()
                if self.__arrow_rect.collidepoint(*pygame.mouse.get_pos()):
                    self._click()
            else:
                for rect in range(len(self.__options_rect)):
                    if self.__options_rect[rect].collidepoint(*pygame.mouse.get_pos()):
                        self._text = self.__current_options[rect]
                self._antiClick()

        if self._state:
            if typing(event):
                if event.unicode == "\x0D":
                        self._antiClick()

    def __configureOptions(self):
        """Determines which options should be displayed at a time"""
        self.__current_options = [option for option in self.__options if option != self._text]

class Checkbox:
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str, size : int = 25, start_state : bool = False):
        """A pygame checkbox"""
        self._screen = screen
        self._identifier = identifier
        
        if start_state:
            self._state = True
            self._bg = self._active_colour
        else:
            self._state = False
            self._bg = self._inactive_colour

        self._rect = pygame.Rect(0, 0, size, size)
        self._rect.center = (x, y)

    def place(self):
        """Places the checkbox on the screen"""
        pygame.draw.rect(self._screen, self._bg, self._rect)
        pygame.draw.rect(self._screen, "#000000", self._rect, 1)
    
    def checkInteract(self, event : pygame.event.Event):
        """Checks for interaction"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                if not self._state:
                    self._click()
                else:
                    self._antiClick()
    
    def _click(self):
        """Updates the box to show a click on"""
        self._bg = self._active_colour
        self._state = True
    
    def _antiClick(self):
        """Updates the box to show a click off"""
        self._bg = self._inactive_colour
        self._state = False
    
    def getIdentifier(self):
        """Returns the associated identifier"""
        return self._identifier
    
    def getValue(self):
        """Returns value"""
        return self._state

class RadioButton(Checkbox):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, dx : int, dy : int, identifier : str, size : int = 25):
        """A pygame radio button"""
        super().__init__(screen, x, y, identifier, size, True)
        self.__rect2 = self._rect.copy()
        self.__rect2.center = (x+dx, y+dy)
        self.__bg2 = self._inactive_colour

    def place(self):
        """Places the radio button on the screen"""
        super().place()
        pygame.draw.rect(self._screen, self.__bg2, self.__rect2)
        pygame.draw.rect(self._screen, "#000000", self.__rect2, 1)

    def __click(self):
        """Updates the box to show a click on"""
        super()._click()
        self.__bg2 = self._inactive_colour
        
    def __antiClick(self):
        """Updates the box to show a click off"""
        super()._antiClick()
        self.__bg2 = self._active_colour
        

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                self.__click()
            elif self.__rect2.collidepoint(*pygame.mouse.get_pos()):
                self.__antiClick()

class ImageBooleanButton:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str, path : str, scale : float = 1.0):
        """A pygame boolean button"""
        self.__screen = screen
        self.__identifier = identifier
        self.__state = False

        self.__shape = pygame.transform.scale_by(pygame.image.load(path), (scale, scale))
        self.__rect, self.__clickable_rect = self.__shape.get_rect(), self.__shape.get_bounding_rect()
        self.__rect.centre = self.__clickable_rect.center = (x, y)

    def place(self):
        """Places the boolean button on the screen"""
        self.__screen.blit(self.__shape, self.__rect)
    
    def checkInteract(self):
        """Checks for interactions"""
        if tapping(event):
            if self.__clickable_rect.collidepoint(*pygame.mouse.get_pos()):
                self.__state = True

    def getIdentifier(self):
        """Returns the associated identifer"""
        return self.__identifier
    
    def getValue(self):
        """Returns value"""
        state = self.__state
        if state:
            self.__state = False
        return state

class DualImageBooleanButton:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, identifier : str, off_path : str, on_path : str, off_scale : float = 1.0, on_scale : float = 1.0):
        self.__screen = screen
        self.__identifier = identifier
        self.__state = False

        self.__off_shape = pygame.transform.scale_by(pygame.image.load(off_path), (off_scale, off_scale))
        self.__off_rect, self.__off_clickable_rect = self.__off_shape.get_rect(), self.__off_shape.get_bounding_rect()

        self.__on_shape = pygame.transform.scale_by(pygame.image.load(on_path), (on_scale, on_scale))
        self.__on_rect, self.__on_clickable_rect = self.__on_shape.get_rect(), self.__on_shape.get_bounding_rect()

        self.__off_rect.center = self.__on_rect.center = self.__off_clickable_rect.center = self.__on_clickable_rect.center = (x, y)

    def place(self):
        """Places the boolean button on the screen"""
        if self.__state:
            self.__screen.blit(self.__on_shape, self.__on_rect)
        else:
            self.__screen.blit(self.__off_shape, self.__off_rect)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""    
        if tapping(event):
            if self.__state:
                if self.__on_clickable_rect.collidepoint(*pygame.mouse.get_pos()):
                    self.__state = False
            else:
                if self.__off_clickable_rect.collidepoint(*pygame.mouse.get_pos()):
                    self.__state = True
    
    def getIdentifier(self):
        """Returns the associated identifier"""
        return self.__identifier

    def getValue(self):
        """Returns value"""
        return self.__state

