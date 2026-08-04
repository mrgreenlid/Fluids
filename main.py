import pygame
from algorithms import *
import interface as ui
import fluid
import numpy as np

import time

pygame.init()

# Sets the constants of the screen surfaced
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1600
FRAME_RATE = 60

bg_colour = "#FFFFFF"
ui_bg = "#ECECEC"


# Initialises database tables
initialiseVelocityFunctionTable()

#initialiseObjectTable()

# JIT Compiles subroutines to be used later on
rotate(np.array([(0,0)]),0)
translate(np.array([(0,0)]), 0, 0)
colourByMagnitude(0.0)


# Creates screen with specific attributes
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load("images\\ui\\icon_image.png"))

# Sets clock to measure and regulate frame rate
clock = pygame.time.Clock()

# Creates variables to be used throughout
data = {"show_control":True,
        "show_objects" : False,
        "flow":False,
        "show_field":True,
        "show_streamline":False,
        "field_rows":16,
        "frame_rate":0.0,
        "show_custom":False,
            "scenario":"tunnel",
            "velocity_function": "",
             "speed":1.0,
             "kinetic_energy": 0.0,
             "force": 0.0,
             "circulation" : 0.0,
             "flux" : 0.0}

# Instantiates control panel components
control_panel_box = ui.Box(screen, SCREEN_WIDTH-175, SCREEN_HEIGHT/2, 350, SCREEN_HEIGHT, ui_bg)
control_panel_label = ui.Label(screen, SCREEN_WIDTH-175, 30, "Control Panel", 30, ui_bg)
speed_label = ui.Label(screen, SCREEN_WIDTH-300, 100, "Speed:", 20, ui_bg)
speed_entry = ui.Entry(screen, SCREEN_WIDTH-200, 100, data["speed"], "speed", float)
speed_unit_label = ui.Label(screen, SCREEN_WIDTH-50, 100,"ms\u207B\u00B9", 21, ui_bg)
show_field_label = ui.Label(screen, SCREEN_WIDTH-265, 150, "Vector field:", 20, ui_bg)
field_rows_increment = ui.Increment(screen, SCREEN_WIDTH-45, 150, "field_rows", data["field_rows"], 32, 2)
show_particle_label = ui.Label(screen, SCREEN_WIDTH-282, 200, "Particles:", 20, ui_bg )
show_grid_doublecheckbox = ui.DoubleCheckbox(screen, SCREEN_WIDTH-100, 150, 0, 50, "show_field")
show_streamline_label = ui.Label(screen, SCREEN_WIDTH-278, 250, "Streamline:", 20, ui_bg)
show_streamline_checkbox = ui.Checkbox(screen, SCREEN_WIDTH-100, 250, "show_streamline")
velocity_function_label = ui.Label(screen, SCREEN_WIDTH-290, 300, "Scenario:", 20, ui_bg)
velocity_function_dropdown = ui.Dropdown(screen, SCREEN_WIDTH-200, 300, ["Tunnel", "Falling", "Vortex", "Custom"], "scenario", str)
custom_vf_label = ui.Label(screen, SCREEN_WIDTH-300, 350, "Custom:", 20, ui_bg)
custom_vf_entry = ui.Entry(screen, SCREEN_WIDTH-240, 350, data["velocity_function"], "velocity_function", str, 22, 230, 17)

select_object_button = ui.Image_Boolean_Button(screen, SCREEN_WIDTH-175, 450, "show_objects", "images\\ui\\select_object.png", (0.5,0.5))

border_data_box = ui.Box(screen,SCREEN_WIDTH-175, 500, 240, 1, "#000000")

energy_label = ui.Label(screen, SCREEN_WIDTH-214, 530, "Kinetic Energy (J):", 17, ui_bg, "Courier")
energy_data = ui.Label(screen, SCREEN_WIDTH-80, 530, 0.0, 17, ui_bg, "Courier", "kinetic_energy")
force_label = ui.Label(screen, SCREEN_WIDTH-245, 560, "Avg Force(N):", 17, ui_bg, "Courier")
force_data = ui.Label(screen, SCREEN_WIDTH-80, 560, 0.0, 17, ui_bg, "Courier", "force")
circulation_label = ui.Label(screen, SCREEN_WIDTH-250, 590, "Circulation:", 17, ui_bg, "Courier")
circulation_data = ui.Label(screen, SCREEN_WIDTH-80, 590, 0.0, 17, ui_bg, "Courier", "circulation")
flux_label = ui.Label(screen, SCREEN_WIDTH-285, 620, "Flux:", 17, ui_bg, "Courier")
flux_data = ui.Label(screen, SCREEN_WIDTH-80, 620, 0.0, 17, ui_bg, "Courier", "flux")
frame_rate_label = ui.Label(screen,SCREEN_WIDTH-222, 650, "Performance (fps):", 17, ui_bg, "Courier")
frame_rate_data = ui.Label(screen,SCREEN_WIDTH-80, 650, 0.0, 17, ui_bg, "Courier", "frame_rate")

control_objects = (control_panel_label, speed_label, speed_entry, speed_unit_label,
                   show_grid_doublecheckbox, show_field_label, show_particle_label, field_rows_increment,
                   show_streamline_label, show_streamline_checkbox, velocity_function_label, velocity_function_dropdown, select_object_button, border_data_box, energy_label, energy_data,force_label,
                   force_data, circulation_label, circulation_data, flux_label, flux_data, frame_rate_label, frame_rate_data,)
                   
control_interactable = (speed_entry, show_grid_doublecheckbox, field_rows_increment, show_streamline_checkbox, velocity_function_dropdown, select_object_button)


# Instantiates object selection components:
back_from_objects_button = ui.Image_Boolean_Button(screen, SCREEN_WIDTH-320, 30, "show_control", "images\\ui\\back_from_objects.png", (0.2, 0.2))

object_objects = (back_from_objects_button, )
object_interactable = (back_from_objects_button,)

# Instantiates tank components
flow_button = ui.Dual_Image_Boolean_Button(screen, 22, 30, "flow", "images\\ui\\play_image.png", "images\\ui\\pause_image.png", (0.2, 0.2), (0.2, 0.2), "space")
vector_field = fluid.VectorField(screen, data["field_rows"], ["show_field", "field_rows", "flow", "speed"])

tank_objects = (vector_field, flow_button)
tank_interactable = (vector_field, flow_button)     

running = True
while running:
    # Changes the caption of the window to view framerate and colours the screen blank, to allow for objects to be placed on it
    pygame.display.set_caption(f"Fluid Mechanics Simulator")
    screen.fill(bg_colour)

    
    # Starts event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        # Sets keybinds for control of the ui
        if typing(event):
            if keys[pygame.K_c]:
                data["show_control"] = toggleVariable(data["show_control"])
                data["show_objects"] = False
            
        # Checks for interactions with different objects, depending
        for obj in tank_interactable:
            if tapping(event) or typing(event):
                if obj.class_type == "input":
                    obj.checkInteract(event, keys)
                    data[obj.getVariable()] = obj.getValue()
            if obj.class_type == "output": 
                obj.setValue(*([data[variable] for variable in obj.getVariable()]))

        
        if data["show_objects"]:
            for obj in object_interactable:
                obj.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                        data[obj.getVariable()] = obj.getValue()  
                
        if data["show_control"]:
            for obj in control_interactable:
                obj.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                    data[obj.getVariable()] = obj.getValue()

            # Checks interaction with bespoke objects 
            if data["scenario"] == "custom":
                custom_vf_entry.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                    data[custom_vf_entry.getVariable()] = custom_vf_entry.getValue()



    # Places objects, when relevant    
    for obj in tank_objects:
            obj.place()
        
    if data["show_control"]:
        
        control_panel_box.place()
        if data["scenario"] == "custom":
            # Places bespoke objects
            custom_vf_label.place()
            custom_vf_entry.place()

        # Sets the velocity function for the vector field
            if searchVelocityFunction(data["velocity_function"]):
                vector_field.setVelocityFunction(searchVelocityFunction(data["velocity_function"])[1:])
            elif validVelocityFunction(data["velocity_function"]):
                saveVelocityFunction(data["velocity_function"])
        else:
            vector_field.setVelocityFunction(searchVelocityFunction(data["scenario"])[1:])

        # Places control objects
        for obj in control_objects:
            obj.place()
            # Updates dynamic labels
            try:
                obj.update(data)
            except AttributeError:
                pass
    
    if data["show_objects"]:
        data["show_control"] = False
        control_panel_box.place()
        for obj in object_objects:
            obj.place()
            
    


    # Updates the screen with changes that have been set in each loop
    pygame.display.flip()

    # Keeps loop in time with the clock
    data["frame_rate"] = clock.get_fps()
    dt = clock.tick(FRAME_RATE) / 1000  

 

pygame.quit()