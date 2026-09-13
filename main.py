import pygame
import interface as ui
from algorithms import *
import fluid as fluid
import numpy as np

pygame.init()

# Sets the constants of the screen
HEIGHT = 900
WIDTH = 1600
BG = "#FFFFFF"
UIBG = "#ECECEC"
FRAMES = 60

# Sets up the pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid mechanics NEA")
screen.fill(BG)
pygame.display.flip()
pygame.display.set_icon(pygame.image.load("images\\ui\\icon_image.png"))

# Creates a clock to measure and regulate frames
clock = pygame.time.Clock()

data = {"flow":False,
        "control":True,
        "body_control":False,

             "field":True,
             "streamline":False,
             "uniform":True,
             "uniform_magnitude":1.0,
             "uniform_angle_raw":"\u03C0", 
             "uniform_angle":1.0,

             "frames":0.0}

control_box = ui.Box(screen, WIDTH-175, HEIGHT//2, 350, HEIGHT, UIBG, True)
control_title_label = ui.Label(screen, WIDTH-175, 30, "Control Panel", 40, bg=UIBG)
show_field_label = ui.Label(screen, WIDTH-270, 100, "Vector field:", 22, bg=UIBG)
field_particle_radiobutton = ui.RadioButton(screen, WIDTH-90, 100, 0, 50, "field")
show_particle_label = ui.Label(screen, WIDTH-280, 150, "Particles:", 22, bg=UIBG)
streamline_label = ui.Label(screen, WIDTH-270, 200, "Streamline:", 22, bg=UIBG)
streamline_checkbox = ui.Checkbox(screen, WIDTH-90, 200, "streamline" )

uniform_label = ui.Label(screen, WIDTH-280, 250, "Uniform:", 22, bg=UIBG)
non_uniform_label = ui.Label(screen, WIDTH-130, 250, "Non-Uniform:", 22, bg=UIBG )
uniform_radiobutton = ui.RadioButton(screen, WIDTH-220, 250, 175, 0, "uniform")

uniform_magnitude_label = ui.Label(screen, WIDTH-268, 300, "Magnitude:", 22, bg=UIBG)
uniform_magnitude_entry = ui.Entry(screen, WIDTH-175, 300, "uniform_magnitude", data["uniform_magnitude"], max_length=6, font="Courier")
uniform_angle_label = ui.Label(screen, WIDTH-290, 350, "Angle:", 22, bg=UIBG)
uniform_angle_composite_entry = ui.CompositeEntry(screen, WIDTH-175, 350, "uniform_angle_raw", data["uniform_angle_raw"], font="Courier")

uniform_magnitude_datalabel = ui.DataLabel(screen, WIDTH-180, 456, "uniform_magnitude", data["uniform_magnitude"], 39, 6, True, "left", bg=UIBG, font="Courier")
e_label = ui.Label(screen, WIDTH-175, 450, "e", 50, bg=UIBG, font="Courier")
i_label = ui.Label(screen, WIDTH-159, 430, "i", 25, bg=UIBG, font="SWital")
open_bracket_label = ui.Label(screen, WIDTH-148, 430, "(", 30, bg=UIBG, font="Courier")
uniform_angle_datalabel = ui.DataLabel(screen, WIDTH-136, 430, "uniform_angle", data["uniform_angle"], 21, max_length=8, bg=UIBG, font="Courier")
close_bracket_label = ui.Label(screen, WIDTH-31, 430, ")", 30, bg=UIBG, font="Courier")

flow_button = ui.DualImageBooleanButton(screen, WIDTH-175, 650, "flow", "images\\ui\\play_image.png", "images\\ui\\pause_image.png", 0.2, 0.2)
control_divider = ui.Box(screen, WIDTH-175, 700, 300, 1)
frames_label = ui.Label(screen, WIDTH-250, 730, "Performance (fps):", bg=UIBG)
frames_datalabel = ui.DataLabel(screen, WIDTH-100, 730, "frames", data["frames"], max_length=8, bg=UIBG)

control_visual = (control_box, control_title_label, 
                  show_field_label, field_particle_radiobutton, show_particle_label,
                  streamline_label, streamline_checkbox, 
                  uniform_label, uniform_radiobutton, non_uniform_label,
                  

                  flow_button, control_divider, frames_label, frames_datalabel)

uniform_visual = (uniform_magnitude_label, uniform_magnitude_entry, 
                  uniform_angle_label, uniform_angle_composite_entry,
                  uniform_magnitude_datalabel, e_label, i_label, open_bracket_label,  uniform_angle_datalabel, close_bracket_label)

control_interact = (field_particle_radiobutton, 
                    streamline_checkbox,
                    uniform_radiobutton, 
                    flow_button)

uniform_interact = (uniform_magnitude_entry, 
                    uniform_angle_composite_entry)


velocity_field = fluid.VelocityField(screen, (WIDTH-350)//2, HEIGHT//2, WIDTH-350, HEIGHT)


tank_visual = (velocity_field, )


running = True
while running:
    screen.fill(BG)

    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    



        if data["control"]:
            for obj in control_interact:
                obj.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                    data[obj.getIdentifier()] = obj.getValue()

            if data["uniform"]:
                for obj in uniform_interact:
                    obj.checkInteract(event)
                    if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                        data[obj.getIdentifier()] = obj.getValue()
                

    # Places visual elements
    for obj in tank_visual:
        obj.place()

    

    if data["control"]:
        for obj in control_visual:
            if isinstance(obj, ui.DataLabel):
                obj.update(data[obj.getIdentifier()])
            obj.place()
        
        if data["uniform"]:
            for obj in uniform_visual:
                if isinstance(obj, ui.DataLabel):
                    obj.update(data[obj.getIdentifier()])
                obj.place() 
        



    # Updates the screen with changes set in the loop
    pygame.display.flip()

    # Keeps the clock ticking
    data["frames"] = clock.get_fps()
    clock.tick(FRAMES) 

pygame.quit()