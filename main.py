import pygame
from algorithms import *
import interface as ui
import fluid

pygame.init()

# Sets the constants of the screen surface
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1600
bg_colour = "#FFFFFF"
ui_bg = "#ECECEC"

# Creates screen with specific attributes
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load("icon_image.png"))

# Sets clock to measure and regulate frame rate
clock = pygame.time.Clock()
dt = 0

# Creates variables to be used throughout
variables = {"tank":True,
             "control_active":True,
             "flow":False,
             "show_field":True,
             "speed":0.0,
             "direction":"left"}


# Instantiates control panel components
control_panel = ui.Box(screen, SCREEN_WIDTH-180, SCREEN_HEIGHT/2, 450, SCREEN_HEIGHT, ui_bg)
control_panel_title = ui.Label(screen, SCREEN_WIDTH-200, 30, "Control Panel", 30, ui_bg)
speed_label = ui.Label(screen, SCREEN_WIDTH-352, 100, "Speed:", 20, ui_bg)
speed_box = ui.Entry(screen, SCREEN_WIDTH-250, 99, 0, "speed", float)
speed_unit_label = ui.Label(screen, SCREEN_WIDTH-100, 100,"ms\u207B\u00B9", 21, ui_bg)
direction_label = ui.Label(screen, SCREEN_WIDTH-330, 150, "Direction:", 20, ui_bg)
direction_dropdown = ui.Dropdown(screen, SCREEN_WIDTH-250, 149, ("Left", "Right", "Up", "Down", "Random"), "direction", str)


show_field_label = ui.Label(screen, SCREEN_WIDTH-315, 210, "Vector field:", 20, ui_bg)
show_particle_label = ui.Label(screen, SCREEN_WIDTH-332, 260, "Particles:", 20, ui_bg )
show_grid_doublecheckbox = ui.DoubleCheckbox(screen, SCREEN_WIDTH-220, 210, 0,50, "show_field")


control_objects = (control_panel, control_panel_title, speed_label, speed_box, speed_unit_label, direction_label,
                   show_grid_doublecheckbox, show_field_label, show_particle_label, direction_dropdown)
control_interactable = (speed_box, direction_dropdown, show_grid_doublecheckbox)


# Instantiates tank components
flow_button = ui.Button(screen, 22, 30, "flow", "play_image.png", "pause_image.png", (0.2, 0.2), (0.2, 0.2), "space")
vector_field = fluid.VectorField(screen, 10, "show_field", variables["show_field"])


tank_objects = [vector_field, flow_button]
tank_interactable = [flow_button, vector_field]



running = True
while running:
    # Changes the caption of the window to view framerate and colours the screen blank, to allow for objects to be placed on it
    pygame.display.set_caption(f"Fluid Mechanics Simulator - FPS: {str(clock.get_fps())[:5]}")
    screen.fill(bg_colour)

    # Starts event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if typing(event):
            if keys[pygame.K_c]:
                variables["control_active"] = toggleVariable(variables["control_active"])
                
        # Checks for interactions with different objects, depending
        if variables["tank"]:
            for obj in tank_interactable:
                if tapping(event) or typing(event):
                    if obj.class_type == "input":
                        variables[obj.getVariable()] = obj.getValue()
                        obj.checkInteract(event, keys)
                if obj.class_type == "output":
                    obj.setValue(variables[obj.getVariable()])
                        
                
        if variables["control_active"]:
            for obj in control_interactable:
                obj.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                    variables[obj.getVariable()] = obj.getValue()

    # Places objects, when relevant
    if variables["tank"]:
        for obj in tank_objects:
            obj.place()
        
    if variables["control_active"]:
        for obj in control_objects:
            obj.place()


    # Updates the screen with changes that have been set in each loop
    pygame.display.flip()

    # Keeps loop in time with the clock
    dt = clock.tick(60) / 1000
    print(variables)
    
pygame.quit()