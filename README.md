# Fluid Simulation
___
This is a project for AQAs A-Level NEA to simulate and visualise 
fluid flow around objects

## Description
___
The project is for Mr Regan to use to demonstrate
fluid flow around certain objects and shapes <br>
There are three main components to the project: the GUI, the mechanics and the event loop.

A few key points to note: the main screen / where the simulation takes place is referred to as the "tank"
## UI Objects / Methods
___

```python
import pygame
from typing import List
```

## Window

Constructor for the Window class which takes attributes for the window:
```python
Window.__init__(window, x, y, width, height, colour)
```

Draws a pygame rect at the prespecified location:
```python
Window.place()
```
___
## Label

Constructor for the Label class. Creates a pygame font object:
```python
Label.__init__(window, x, y, text, size, bg)
```

Places the font object at the prespecified location:
```python
Label.place()
```
___
## Entry(Label, Usable)

Constructor for the Entry class. Uses Label inheritance to create font object. Adjusts the rect to standardise:
```python
Entry.__init__(window, x, y, text, variable, datatype, size)
```

Places a label on a drawn, bordered rectangle:
```python
Entry.place()
```

Changes the box's colour to an "active" blue to show that it is active. Sets the state of self._in_use to True and updates the text:
```python
Entry._click()
```

Changes the box's colour to an "inactive" white to show that it is inactive. Sets the state of self._in_use to False and updates the text:
```python
Entry._antiClick()
```

Checks, before updating, the data in the box for syntax and logic errors:
```python
Entry.__errorCorrect()
```

Checks for errors, using self.errorCorrect() then updates the text's render arguments:
```python
Entry._updatepython()
```

Updates self._text based on keydown events: 
```python
Entry._typeText(event)
```

Uses the inherited tapping and typing functions, each tick, to check for interaction with the box:
```python
Entry.checkInteract(event)
```

Returns the name of the variable the box affects:
```python
Entry.getVariable()
```

Returns the contents of the textbox, cast in the correct datatype:
```python
Entry.getValue()
```
___
## Dropdown(Entry)

Constructor for the Dropdown class. Creates font objects and boxes for each option and makes a dropdown button:
```python
Dropdown.__init__(window, x, y, options, variable, datatype)
```

Draws the main box, inherited from Entry and the options when it is in use in the prespecified location:
```python
Dropdown.place()
```

Uses the tapping and typing functions, each tick, to check for interaction with the boxs and dropdown button:
```python
Dropdown.checkInteract(event)
```
___
## Checkbox(Usable)

Constructor for Checkbox class. Creates rect for the box:
```python
Checkbox.__init__(window, x, y,variable)
```

Draws the bordered checkbox in the prespecified location:
```python
Checkbox.place()
```

Changes the box's colour to an "active" blue to show that it is active. Sets the state of self.__state to True:
```python
Checkbox._click()
```

Changes the box's colour to an "inactive" white to show that it is inactive. Sets the state of self.__state to False:
```python
Checkbox._antiClick()
```

Uses the tapping and typing functions, each tick, to check for interaction with the box:
```python
Checkbox.checkInteract(event)
```

___
## Button
Constructor for Button class. Creates on and off state image objects and sets up a keybind if provided
```python
Button.__init__(window, x,  y, variable, path_1, path_2, scale_factor_1, scale_factor_2, key_bind)
```

Blits the image, at the set scale, in the prespecified location
```python
Button.place()
```

Uses tapping and typing functions to, each tick, to check for interactions with the button and whether the bound key had been pressed
```python
Button.checkInteract(event)
```

