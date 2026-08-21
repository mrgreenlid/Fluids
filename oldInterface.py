import pygame
from algorithms import *
from typing import Tuple, List
import re

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

class Label(Output):
    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, size : int, bg : str, font : str = "Consolas", variable : str = None):
        """Creates text label to be placed on screen"""
        self._window = window
        self._size = size
        self._bg = bg
        self._text = f"{text}"
        self.__variable = variable
    
        # Creates a set of arguments to be used to render the text
        self._render_arguments = [self._text, True, "#000000", self._bg]

        # Creates the font object, rect and sets position
        self._font = pygame.font.SysFont(font, self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x,y)

    def place(self):
        """Places label at preset location"""
        self._window.blit(self._font.render(*self._render_arguments), self._rect)
    
    def update(self, data):
        """Applies changes to the label if the parameters have changed"""
        try:
            if isinstance(data[self.__variable], float):
                self._render_arguments[0] = str('{0:.10f}'.format(data[self.__variable]))[:7]
        except KeyError:
            pass

class Entry(Label, Input):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"
    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, variable : str, datatype : type, size : int = 25, width : int = 120, text_length : int = 10):
        """Creates entry box to be placed on screen"""
        super().__init__(window, x, y, " ", size, self._inactive_colour, "Courier")
        self._text = f"{text}"
        self._variable = variable
        self._datatype = datatype
        self._in_use = False
        self._text_length = text_length

        # Lengthens the box 
        self._rect.width = width
        self.__updateText()

    def place(self):
        """Places entry box at preset location"""
        pygame.draw.rect(self._window, self._bg, self._rect)
        super().place()
        pygame.draw.rect(self._window, "#000000", self._rect, 1)

    def _click(self):
        """Changes box to active colours"""
        self._bg = self._active_colour
        self._in_use = True
        self.__updateText()

    def _antiClick(self):
        """Changes box to inactive colours"""
        self._bg = self._inactive_colour
        self._in_use = False
        self.__updateText()

    def __errorCorrect(self):
        """Checks text for syntax and logic errors"""
        if self._datatype == float:
            
            if not self._in_use:
                if len(self._text) == 0:
                    self._text = "0"
                elif self._text[-1] == ".":
                    self._text = self._text[:-1]
            
            if re.match("^0+[0-9]", self._text):
                self._text = self._text[1:]
            
            if len(self._text) > 6 :
                self._text = self._text[:6]

        if self._datatype == str:
            if len(self._text) > self._text_length:
                self._text = self._text[:-1]
                        

    def __updateText(self):
        """Cements changes to text"""
        self.__errorCorrect()
        self._render_arguments[0], self._render_arguments[3] = self._text, self._bg

    def _typeText(self, event):
        """Changes text by keyboard input"""
        key = event.unicode

        if key == "\x08":
            self._text = self._text[:-1]

        elif key == "\x0D":
            self.__updateText()
            self._antiClick()

        elif self._datatype == float:
            if key.isdigit() or (key == "." and "." not in self._text):
                self._text += key
        
        elif self._datatype == str: 
            self._text += key

        self.__updateText()

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self._rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                self._click()

            else:
                self.__updateText()
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
            try:
                return float(self._text)
            except ValueError:
                self._text = "0"
                return float(self._text)
                
        elif self._datatype == str:
            return self._text.lower()
        return None

class Dropdown(Entry):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, options : Tuple[str], variable : str, datatype : type):
        """Draws main box and button"""
        super().__init__(window, x, y, options[0], variable, datatype)

        self.__options = options
        self.__options_rect = [self._rect.copy() for _ in range(len(self.__options)-1)]
        for rect in range(len(self.__options)-1):
            self.__options_rect[rect].centery += (30*(rect+1))

        self.__arrow_rect = pygame.Rect(0, 0, 30, 30)
        self.__arrow_rect.center = (x + 140, y + 1)
        self.__arrow_coordinates = [(self.__arrow_rect.centerx, self.__arrow_rect.centery + 2.5),
                                    (self.__arrow_rect.centerx + 5, self.__arrow_rect.centery - 2.5),
                                    (self.__arrow_rect.centerx - 5, self.__arrow_rect.centery - 2.5)]

    def place(self):
        """Draws text box and options at appropriate times"""
        super().place()
        pygame.draw.rect(self._window, "#D3D3D3", self.__arrow_rect)
        pygame.draw.rect(self._window, "#000000", self.__arrow_rect, 1)
        pygame.draw.polygon(self._window, "#000000", self.__arrow_coordinates)
        if self._in_use:
            current_options = [option for option in self.__options if option != self._text]
            for rect in range(len(current_options)):
                pygame.draw.rect(self._window, "#FFFFFF", self.__options_rect[rect], 0)
                self._window.blit(self._font.render(current_options[rect], True, "#000000", "#FFFFFF"), self.__options_rect[rect])
                pygame.draw.rect(self._window, "#000000", self.__options_rect[rect], 1)

    def checkInteract(self, event : pygame.event.Event):
            """Checks for interactions"""
            current_options = [option for option in self.__options if option != self._text]
            if tapping(event):
                if not self._in_use:
                    if self.__arrow_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                        self._click()
                else:
                    for rect in range(len(self.__options_rect)):
                        if self.__options_rect[rect].collidepoint(*pygame.mouse.get_pos()[:2]):
                            self._text = current_options[rect]
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


class Image_Boolean_Button(Input):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str, image_path : str, scale_factor : Tuple[int] = (1,1), key_bind : str = None):
        """Creates image button to be placed on screen"""
        self.__window = window
        self.__variable = variable
        self.__state = False

        self.__shape = pygame.transform.scale_by(pygame.image.load(image_path).convert_alpha(), scale_factor)
        self.__clickable_rect = self.__shape.get_bounding_rect()
        self.__rect = self.__shape.get_rect()
        self.__rect.center = self.__clickable_rect.center = (x,y)
        
    
        try:
            self.__key_bind = pygame.key.key_code(key_bind)
        except TypeError:
            self.__key_bind = False


    def place(self):
        """Blits the image of the button"""
        self.__window.blit(self.__shape, self.__rect)
        
    
    def checkInteract(self, event : pygame.event.Event, keys : List[bool] = None):
        """Checks for interactions"""
        if tapping(event):
            if self.__clickable_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                self.__state = True
             
        if self.__key_bind:
            if typing(event):
                if keys[self.__key_bind]:
                    self.__state = toggleVariable(self.__state)


    def __flip(self):
        """Forces the variable to flip states"""
        self.__state = toggleVariable(self.__state)

    def getVariable(self):
        """Returns associated variable"""
        return self.__variable


    def getValue(self):
        """Returns value"""
        state = self.__state
        if state:
            self.__flip()
        return state


            
class Dual_Image_Boolean_Button(Input):
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str, path_1 : str, path_2 : str, scale_factor_1 : Tuple[int] = (1,1), scale_factor_2 : Tuple[int] = (1,1), key_bind : str = None):
        """Creates dual image button to be placed on screen"""
        self.__window = window
        self.__variable = variable
        self.__state = False

        self.__off_shape = pygame.transform.scale_by(pygame.image.load(path_1).convert_alpha(), scale_factor_1)
        self.__off_rect = self.__off_shape.get_rect()
        self.__off_clickable_rect = self.__off_shape.get_bounding_rect()
        self.__off_rect.center = self.__off_clickable_rect.center =(x, y)
        
   
    
        self.__on_shape = pygame.transform.scale_by(pygame.image.load(path_2).convert_alpha(), scale_factor_2)
        self.__on_rect = self.__on_shape.get_rect()
        self.__on_clickable_rect = self.__on_shape.get_bounding_rect()
        self.__on_rect.center = self.__on_clickable_rect.center = (x, y)

           
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

    def checkInteract(self, event : pygame.event.Event, keys : List[bool] = None):
        """Checks for interactions"""
        if tapping(event):
            if self.__state:
                if self.__on_clickable_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                    self.__state = False
            else:
                if self.__off_clickable_rect.collidepoint(*pygame.mouse.get_pos()[:2]):
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


class BodySelectionButton(Input):
    __variable = "body_index"
    def __init__(self, window, x : int, y : int, index : int, image_scale_factor : Tuple[int, int]):
        """Creates bespoke button to be placed on screen"""
        self.__window = window
        self.__index = index

        properties = getBodyProperties(index)[0:2]
        
        self.__click_flag = False


        self.__name = properties[0][0].upper() + properties[0][1:]
        self.__path = properties[1]
      
        self.__rect = pygame.rect.Rect(0,0, 150, 100)
        self.__rect.center = (x,y)  
        
        self.__image = pygame.transform.scale_by(pygame.image.load(self.__path).convert_alpha(), image_scale_factor)
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.center = (x,y)

        self.__font = pygame.font.SysFont("consolas", 20)
        self.__text_rect = self.__font.render(self.__name, True, "#000000", "#FFFFFF").get_rect()
    
        self.__text_box_rect = self.__text_rect.copy()
        self.__text_box_rect.width = 150
        self.__text_box_rect.height = 30
        self.__text_box_rect.center = self.__text_rect.center = (x, y + 75)
       

    def place(self):
        """Draws body selection button"""
        pygame.draw.rect(self.__window, "#FFFFFF", self.__rect)
        pygame.draw.rect(self.__window, "#000000", self.__rect, 1)
        self.__window.blit(self.__image, self.__image_rect)
        pygame.draw.rect(self.__window, "#FFFFFF", self.__text_box_rect)
        pygame.draw.rect(self.__window, "#000000", self.__text_box_rect, 1)
        self.__window.blit(self.__font.render(self.__name, True, "#000000", "#FFFFFF"), self.__text_rect)

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self.__rect.collidepoint(*pygame.mouse.get_pos()):
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
        """Returns associated variable"""
        return self.__variable
    
    def getValue(self):
        """Returns value"""
        return self.__value