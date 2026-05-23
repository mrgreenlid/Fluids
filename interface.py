import pygame
from algorithms import toggleVariable
from typing import Tuple, List

class Window:
    def __init__(self, window : pygame.Surface, x : int, y : int, width : int, height : int, colour : str):
        """Creates window to be placed on screen"""
        self.__window = window

        self.__colour = colour
        self.__rect = pygame.Rect(0, 0, width, height)
        self.__rect.center = (x,y)

    def place(self):
        """Draws window at preset location"""
        pygame.draw.rect(self.__window, self.__colour, self.__rect)


def tapping(event : pygame.event.Event):
    """Checks for tapping"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    return False

def typing(event : pygame.event.Event):
    """Checks for typing"""
    if event.type == pygame.KEYDOWN:
        return True
    return False

class Label:
    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, size : int, bg : str):
        """Creates text label to be placed on screen"""
        self._window = window

        self._size = size
        self._bg = bg
        self._text = f"{text}"

        # Creates a set of arguments to be used to render the text
        self._render_arguments = [self._text, True, "black", self._bg]

        # Creates the font object, rect and sets position
        self._font = pygame.font.SysFont("Consolas", self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x,y)

    def place(self):
        """Places label at preset location"""
        self._window.blit(self._font.render(*self._render_arguments), self._rect)

class Entry(Label):
    _inactive_colour = "#FFFFFF"
    _active_colour = "#90D5FF"

    def __init__(self, window : pygame.Surface, x : int, y : int, text : str, variable : str, datatype : type, size : int = 25):
        """Creates entry box to be placed on screen"""
        super().__init__(window, x, y, " ", size, self._inactive_colour)

        self._text = f"{text}"

        self._variable = variable
        self._datatype = datatype

        self._in_use = False

        # Creates font object, rect and sets position
        self._font = pygame.font.SysFont("Courier", self._size)
        self._rect = self._font.render(*self._render_arguments).get_rect()
        self._rect.center = (x, y)

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

class Dropdown(Entry):
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

class Checkbox:
    __inactive_colour = "#FFFFFF"
    __active_colour = "#90D5FF"

    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str):
        """Creates checkbox to be placed on screen"""
        self.__window = window

        self.__variable = variable

        self.__state = False
        self.__bg = self.__inactive_colour


        self.__rect = pygame.Rect(0, 0, 25, 25)
        self.__rect.center = (x, y)

    def place(self):
        """Draws checkbox, with border"""
        pygame.draw.rect(self.__window, self.__bg, self.__rect)
        pygame.draw.rect(self.__window, "#000000", self.__rect, 1)

    def __click(self):
        """Changes box to active colours"""
        self.__bg = self.__active_colour
        self.__state = True

    def __antiClick(self):
        """Changes box to inactive colours"""
        self.__bg = self.__inactive_colour
        self.__state = False

    def checkInteract(self, event : pygame.event.Event):
        """Checks for interactions"""
        if tapping(event):
            if self.__rect.collidepoint(*pygame.mouse.get_pos()[:2]):
                if self.__state:
                    self.__antiClick()
                else:
                    self.__click()


    def getVariable(self):
        """Returns associated variable"""
        return self.__variable

    def getValue(self):
        """Returns value"""
        return self.__state

class Button:
    def __init__(self, window : pygame.surface.Surface, x : int, y : int, variable : str, path_1 : str, path_2 : str, scale_factor_1 : Tuple[int] = None, scale_factor_2 : Tuple[int] = None, key_bind : str = None):
        self.__window = window
        self.__variable = variable

        self.__state = False

        self.__off_shape = pygame.transform.scale_by(pygame.image.load(path_1).convert_alpha(), scale_factor_1)
        self.__off_rect = self.__off_shape.get_rect()
        self.__off_rect.center = (x, y)

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