import pygame
from algorithms import *
import re
from typing import Tuple, List
import databaseManagement as db


class Box:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, width : int, height : int, colour : str, outline : bool = False):
        """A pygame box"""
        self.__screen = screen
        self.__colour = colour
        self.__rect = pygame.Rect(x-(width//2), y-(height//2), width, height)

        self.__outline = outline

    def place(self):
        """Places box on the screen"""
        pygame.draw.rect(self.__screen, self.__colour, self.__rect)
        if self.__outline:
            pygame.draw.rect(self.__screen, "#000000", self.__rect, 1)

class Label:
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, text : str, size : int = 20, colour : str = "#000000", bg : str = "#FFFFFF", font : str = "Consolas"):
        """A pygame label"""
        self._screen = screen
        
        self._size = size
        self._color = colour
        self._bg = bg

        self._render_arguments = [f"{text}", True, self._color, self._bg]
        
        self._font = pygame.font.SysFont(font, self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x, y)

    def place(self):
        """Places label on the screen"""
        self._screen.blit(self._font.render(*self._render_arguments), self._rect)



class DataLabel(Label, Output):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, text : str, variable : str,  size : int = 20,  colour : str = "#000000", bg : str = "#FFFFFF", font : str = "Consolas",  dtype : type = float):
        """A pygame data label"""
        super().__init__(screen, x, y, " ", size, colour, bg, font)
        self._text = f"{text}"

        self.__variable = variable
        self.__dtype = dtype
        
    def update(self, new_text):
        """Updates the text"""
        if self.__dtype == float:
            self._render_arguments[0] = f"{new_text:.{10}f}"[:7]
        else:
            self._render_arguments[0] = new_text

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    
class Entry(Label, Input):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, text : str, variable : str, max_length : int = 10, width : int = 120, dtype : type = float):
        """A pygame entry box"""
        super().__init__(screen, x, y, " ", 25, "#000000", self._inactive_colour, "Courier")
        self._text = f"{text}"
        self._max_length = max_length
        self._rect.width = width

        self._dtype = dtype
        self._variable = variable
        self._state = False
    
        self._updateText()

    
    def place(self):
        """Places entry box on the screen"""
        pygame.draw.rect(self._screen, self._bg, self._rect)
        super().place()
        pygame.draw.rect(self._screen, "#000000", self._rect, 1)

    def _updateText(self):
        """Updates the text"""
        if self._dtype == float:
            if not self._state:
                if len(self._text) == 0:
                    self._text = "0"
        
            if re.match("^0+[0-9]", self._text):
                    self._text = self._text[1:]
            
        if len(self._text) > self._max_length :
                    self._text = self._text[:-1]

        self._render_arguments[0] = self._text
        self._render_arguments[3] = self._bg

    def _click(self):
        """Updates the box to show a click on"""
        if not self._state:
            self._bg = self._active_colour
            self._state = True
            self._updateText()
    
    def _antiClick(self):
        """Updates the box to show a click off"""
        if self._state:
            self._bg = self._inactive_colour
            self._state = False
            self._updateText()

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                self._click()
            else:
                self._antiClick()
            
        if self._state:
            if typing(event):
                # Changes the text stored in the textbox
                    key = event.unicode

                    if key == "\x08":
                        self._text = self._text[:-1]
                    elif key == "\x0D":
                        self._antiClick() 
                            
                    elif self._dtype == float and (key.isdigit() or (key == "." and "." not in self._text)):
                        self._text += key
                    elif self._dtype == str:
                        self._text += key
                    
                    self._updateText()

    def getVariable(self):
        """Returns associated variable"""
        return self._variable
    
    def getValue(self):
        """Returns associated value"""
        if self._dtype == float:
            try:
                return float(self._text)
            except ValueError:
                return 0.0
        elif self._dtype == str:
            return self._text.lower()
        return None

class Dropdown(Entry):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, options : Tuple[str] | Tuple[int], variable : str, max_length : int = 10, width : int = 120, dtype : type = float):
        """A pygame dropdown box"""
        super().__init__(screen, x, y, options[0], variable, max_length, width, dtype)
        self.__options = options
        self.__options_rect = []
        self.__current_options = []

        for option in range(len(self.__options)-1):
            self.__options_rect.append(self._rect.copy())
            self.__options_rect[option].centery += 30*(option+1)

        self.__arrow_rect = pygame.Rect(x+125, y-14, 30, 30)
        self.__arrow_coordinates = [(self.__arrow_rect.centerx, self.__arrow_rect.centery + 2.5),
                                    (self.__arrow_rect.centerx + 5, self.__arrow_rect.centery - 2.5),
                                    (self.__arrow_rect.centerx - 5, self.__arrow_rect.centery - 2.5)]

    def place(self):
        """Places dropdown box on the screen"""
        super().place()
        pygame.draw.rect(self._screen, "#D3D3D3", self.__arrow_rect)
        pygame.draw.rect(self._screen, "#000000", self.__arrow_rect, 1)
        pygame.draw.polygon(self._screen, "#000000", self.__arrow_coordinates)

        if self._state:
            for option in range(len(self.__current_options)):
                pygame.draw.rect(self._screen, "#FFFFFF", self.__options_rect[option], 0)
                self._screen.blit(self._font.render(self.__current_options[option], True, "#000000", "#FFFFFF"), self.__options_rect[option])
                pygame.draw.rect(self._screen, "#000000", self.__options_rect[option], 1)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if not self._state:
                self.__configOptions()
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

    def __configOptions(self):
        """Determines the correct current options to display"""
        self.__current_options = [option for option in self.__options if option != self._text]

class Checkbox(Input):
    _active_colour = "#90D5FF"
    _inactive_colour = "#FFFFFF"
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, variable : str, start_state : bool = False):
        """A pygame checkbox"""

        self._screen = screen
        self._variable = variable

        if start_state:
            self._state = True
            self._bg = self._active_colour
        else:
            self._state = False
            self._bg = self._inactive_colour

        self._rect = pygame.Rect(0,0,25,25)
        self._rect.center = (x, y)

    def place(self):
        """Places the checkbox on the screen"""
        pygame.draw.rect(self._screen, self._bg, self._rect)
        pygame.draw.rect(self._screen, "#000000", self._rect, 1)

    def _click(self):
        """Updates the box to show a click on"""        
        self._state = True
        self._bg = self._active_colour

    def _antiClick(self):
        """Updates the box to show a click off"""        
        self._state = False
        self._bg = self._inactive_colour
    
    def checkInteract(self, event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                if not self._state:
                    self._click()
                else:
                    self._antiClick()
    
    def getVariable(self):
        """Returns associated variable"""
        return self._variable
    
    def getValue(self):
        """Returns associated value"""
        return self._state
                
class RadioButton(Checkbox):
    def __init__(self, screen : pygame.surface.Surface,  x : int, y : int, dx : int, dy : int, variable : str):
        """A pygame checkbox"""
        super().__init__(screen, x, y, variable, True)

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
        self._bg = self._active_colour
        self.__bg2 = self._inactive_colour
        self._state = True

    def __antiClick(self):
        """Updates the box to show a click off"""
        self._bg = self._inactive_colour
        self.__bg2 = self._active_colour
        self._state = False

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()):
                self.__click()
            elif self.__rect2.collidepoint(*pygame.mouse.get_pos()):
                self.__antiClick()
    

class ImageBooleanButton(Input):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, variable : str,  path : str, scale : float = 1.0):
        """A pygame boolean button"""
        self.__screen = screen
        self.__variable = variable
        self.__state = False

        self.__shape = pygame.transform.scale_by(pygame.image.load(path), (scale, scale))
        self.__rect, self.__clickable_rect = self.__shape.get_rect(), self.__shape.get_bounding_rect()
        self.__rect.center = self.__clickable_rect.center = (x, y)

    def place(self):
        """Places the boolean button on the screen"""
        self.__screen.blit(self.__shape, self.__rect)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self.__clickable_rect.collidepoint(*pygame.mouse.get_pos()):
                    self.__state = True

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable

    def getValue(self):
        """Returns associated value"""
        state = self.__state
        if state:
            self.__state = not self.__state    
        return state

class DualImageBooleanButton(Input):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, variable : str, path1 : str, path2 : str, scale1 : float = 1.0, scale2 : float = 1.0):
        """A pygame two image state boolean button"""
        self.__screen = screen
        self.__variable = variable
        self.__state = False

        self.__off_shape = pygame.transform.scale_by(pygame.image.load(path1), (scale1, scale1))
        self.__off_rect, self.__off_clickable_rect = self.__off_shape.get_rect(), self.__off_shape.get_bounding_rect()
        
        self.__on_shape = pygame.transform.scale_by(pygame.image.load(path2), (scale2, scale2))
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

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable

    def getValue(self):
        """Returns associated value"""
        return self.__state

class Increment(Input):
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, dx : int, dy : int, variable : str, minimum : float, maximum : float, increment : float):
        """A pygame increment button"""

        self.__screen = screen
        self.__variable = variable
        self.__maximum = maximum
        self.__value = self.__minimum = minimum
        self.__increment = increment

        self.__up_rect = pygame.rect.Rect(0, 0, 25, 25)
        self.__down_rect = self.__up_rect.copy()
        self.__up_rect.center, self.__down_rect.center = (x, y), (x+dx, y+dy)

        self.__up_arrow_coordinates = [(self.__up_rect.centerx, self.__up_rect.centery-2.5),
                                        (self.__up_rect.centerx -5, self.__up_rect.centery + 2.5),
                                        (self.__up_rect.centerx +5, self.__up_rect.centery +2.5)]
        
        self.__down_arrow_coordinates = [(self.__down_rect.centerx, self.__down_rect.centery+2.5),
                                        (self.__down_rect.centerx -5, self.__down_rect.centery - 2.5),
                                        (self.__down_rect.centerx +5, self.__down_rect.centery -2.5)]

    def place(self):
        """Places the increment buttons on the screen"""
        pygame.draw.rect(self.__screen, "#D3D3D3", self.__up_rect)
        pygame.draw.rect(self.__screen, "#000000", self.__up_rect, 1)
        pygame.draw.polygon(self.__screen, "#000000", self.__up_arrow_coordinates)
        pygame.draw.rect(self.__screen, "#D3D3D3", self.__down_rect)
        pygame.draw.rect(self.__screen, "#000000", self.__down_rect, 1)
        pygame.draw.polygon(self.__screen, "#000000", self.__down_arrow_coordinates)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self.__up_rect.collidepoint(*pygame.mouse.get_pos()):
                if (self.__value + self.__increment) <= self.__maximum:
                    self.__value += self.__increment
            elif self.__down_rect.collidepoint(*pygame.mouse.get_pos()):
                if (self.__value - self.__increment) >= self.__minimum:
                    self.__value -= self.__increment

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    def getValue(self):
        """Returns associated value"""
        return self.__value


class BodySelectionButton(Input):
    __variable = "body_index"
    def __init__(self, screen : pygame.surface.Surface, x : int, y : int, index : int, image_scale : float):
        """A pygame button, for one specific purpose"""
        self.__screen = screen
        self.__index = index

        properties = db.getBodyProperties(index)[0:2]

        self.__name = properties[0][0].upper() + properties[0][1:].lower()
        path = properties[1]

        self.__click_flag = False

        self.__rect = pygame.rect.Rect(0,0, 150, 100)
        self.__image = pygame.transform.scale_by(pygame.image.load(path), (image_scale, image_scale))
        self.__image_rect = self.__image.get_rect()
        self.__rect.center = self.__image_rect.center = (x,y)

        self.__font = pygame.font.SysFont("consolas", 20)
        self.__text_rect = self.__font.render(self.__name, True, "#000000", "#FFFFFF").get_rect()
        self.__text_box_rect = self.__text_rect.copy()
        self.__text_box_rect.width = 150
        self.__text_box_rect.height = 30
        self.__text_box_rect.center = self.__text_rect.center = (x, y + 75)

    def place(self):
        """Draws body selection button"""
        pygame.draw.rect(self.__screen, "#FFFFFF", self.__rect)
        pygame.draw.rect(self.__screen, "#000000", self.__rect, 1)
        self.__screen.blit(self.__image, self.__image_rect)
        pygame.draw.rect(self.__screen, "#FFFFFF", self.__text_box_rect)
        pygame.draw.rect(self.__screen, "#000000", self.__text_box_rect, 1)
        self.__screen.blit(self.__font.render(self.__name, True, "#000000", "#FFFFFF"), self.__text_rect)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self.__rect.collidepoint(*pygame.mouse.get_pos()) or self.__text_box_rect.collidepoint(*pygame.mouse.get_pos()):
                self.__click_flag = True
                
    def getClickFlag(self):
        """Returns whether the button was clicked more recently than a call of self.getValue()"""
        return self.__click_flag

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable
    
    def getValue(self):
        """Returns value"""
        self.__click_flag = False
        return self.__index
        