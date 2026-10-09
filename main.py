import pygame
import interface as ui
from algorithms import *
import fluid as fluid
import numpy as np

pygame.init()

# Sets the constants of the screen
HEIGHT = 900
WIDTH = 1550
FIELD_HEIGHT = 900
FIELD_WIDTH = 1200
BG = "#FFFFFF"
UIBG = "#ECECEC"
FRAMES = 60

# Sets up the pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid mechanics NEA")
screen.fill(BG)
pygame.display.flip()
pygame.display.set_icon(pygame.image.load("images\\ui\\icon.png"))


# Test data for initialisation
pixels = np.full((FIELD_WIDTH, FIELD_HEIGHT), 16777215, dtype=np.int32)
positions = np.full((FIELD_WIDTH, FIELD_HEIGHT, 2), -1, dtype=np.float64)
velocity = np.full((FIELD_HEIGHT, FIELD_WIDTH), 1 + 1j, dtype=np.complex64)

# JITs numba decorated functions
mapParticles(positions, velocity, 0.001)

# Creates a clock to measure and regulate frames
clock = pygame.time.Clock()

data = {"flow":False,
        "control":True,
        "body_control":False,
        "fill":False,
        "streamline":False,
        "uniform":True,

        "previous_uniform_magnitude":10.0,
        "uniform_magnitude":10.0,
        
        "previous_raw_uniform_argument" : "π",
        "raw_uniform_argument" : "π",
        "uniform_argument": np.pi,
        
        "previous_non_uniform_flow_name":"",
        "non_uniform_flow_name":"",

             "frames":0.0,
             "dt":0.0}

control_box = ui.Box(screen, WIDTH-175, HEIGHT//2, 350, HEIGHT, UIBG, True)
control_title_label = ui.Label(screen, WIDTH-175, 30, "Control Panel", 40, bg=UIBG)

control_divider = ui.Box(screen, WIDTH-175, 90, 300, 1)
streamline_label = ui.Label(screen, WIDTH-270, 110, "Streamline:", 22, bg=UIBG)
streamline_checkbox = ui.Checkbox(screen, WIDTH-90, 110, "streamline" )
uniform_label = ui.Label(screen, WIDTH-280, 160,  "Uniform:", 22, bg=UIBG)
non_uniform_label = ui.Label(screen, WIDTH-260, 210, "Non-Uniform:", 22, bg=UIBG )
uniform_radiobutton = ui.RadioButton(screen, WIDTH-90, 160, 0, 50, "uniform")



function_divider = ui.Box(screen, WIDTH-175, 240, 320, 1)
uniform_magnitude_label = ui.Label(screen, WIDTH-268, 280, "Magnitude:", 22, bg=UIBG)
uniform_magnitude_entry = ui.Entry(screen, WIDTH-175, 280, "uniform_magnitude", data["uniform_magnitude"], max_length=6, font="Courier")
uniform_argument_label = ui.Label(screen, WIDTH-270, 340, "Angle (rad):", 22, bg=UIBG)
uniform_argument_composite_entry = ui.CompositeEntry(screen, WIDTH-175, 340, "raw_uniform_argument", data["raw_uniform_argument"], 25, ("π", "e"), ((100, 35), (130, 35)), (20,20), 25, button_font="Courier", max_length=9,  dtype=str, font="Courier")
velocity_funtion_label = ui.Label(screen, WIDTH-240, 400, "Velocity function:", 22, bg=UIBG)
uniform_magnitude_datalabel = ui.DataLabel(screen, WIDTH-194, 474, "uniform_magnitude", data["uniform_magnitude"], 30, 6, True, "left", bg=UIBG, font="Courier")
times_label = ui.Label(screen, WIDTH-195, 474, "\u00D7", 30,  bg=UIBG, font="Courier")
e_label = ui.Label(screen, WIDTH-175, 470, "e", 36, bg=UIBG, font="Courier")
i_label = ui.Label(screen, WIDTH-159, 455, "i", 22, bg=UIBG, font="SWital")
open_bracket_label = ui.Label(screen, WIDTH-148, 455, "(", 30, bg=UIBG, font="Courier")
uniform_argument_datalabel = ui.DataLabel(screen, WIDTH-135, 455, "uniform_argument", data["uniform_argument"], 21, max_length=6, bg=UIBG, font="Courier")
close_bracket_label = ui.Label(screen, WIDTH-55, 455, ")", 30, bg=UIBG, font="Courier")


non_uniform_flow_selection_1 = ui.ImageTitleButton(screen, WIDTH-251, 330, "non_uniform_flow_name", "Point Source", "point_source", "images\\flow\\point_source.png", 0.19)
non_uniform_flow_selection_2 = ui.ImageTitleButton(screen, WIDTH-99, 330, "non_uniform_flow_name", "Vortex", "vortex", "images\\flow\\vortex.png", 0.29)
non_uniform_flow_selection_3 = ui.ImageTitleButton(screen, WIDTH-251, 511, "non_uniform_flow_name", "Doublet", "doublet", "images\\flow\\doublet.png", 0.29, -90)

flow_button = ui.DualImageBooleanButton(screen, WIDTH-175, 650, "flow", "images\\ui\\play.png", "images\\ui\\pause.png", 0.1, 0.14)
data_divider = ui.Box(screen, WIDTH-175, 700, 300, 1)
frames_label = ui.Label(screen, WIDTH-250, 730, "Performance (fps):", bg=UIBG)
frames_datalabel = ui.DataLabel(screen, WIDTH-100, 730, "frames", data["frames"], max_length=8, bg=UIBG)

control_visual = (control_box, control_title_label, 
                    control_divider,
                  
                  streamline_label, streamline_checkbox, 
                  uniform_label, uniform_radiobutton, non_uniform_label,
                  function_divider,
                
                  
                  flow_button, data_divider, frames_label, frames_datalabel)

uniform_visual = (velocity_funtion_label, uniform_magnitude_label, uniform_magnitude_entry, 
                  uniform_argument_label, uniform_argument_composite_entry,
                  uniform_magnitude_datalabel, times_label,  e_label, i_label, open_bracket_label,  uniform_argument_datalabel, close_bracket_label)


non_uniform_visual = (non_uniform_flow_selection_1, non_uniform_flow_selection_2, 
                    non_uniform_flow_selection_3)

control_interact = (streamline_checkbox,
                    uniform_radiobutton, 
                    flow_button)

uniform_interact = (uniform_magnitude_entry, 
                    uniform_argument_composite_entry)

non_uniform_interact = (non_uniform_flow_selection_1, non_uniform_flow_selection_2, 
                    non_uniform_flow_selection_3)


velocity_field = fluid.VelocityField(screen, (WIDTH-350)//2, HEIGHT//2, FIELD_WIDTH, FIELD_HEIGHT)


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
                if tapping(event) or typing(event):
                    data[obj.getIdentifier()] = obj.getValue()
        
            if data["uniform"]:
                for obj in uniform_interact:
                    obj.checkInteract(event)
                    if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                        data[obj.getIdentifier()] = obj.getValue()

                        if not (data["previous_uniform_magnitude"] == data["uniform_magnitude"] and data["previous_raw_uniform_argument"] == data["raw_uniform_argument"]):
                            if validExpression(valid_angle_rule, data["raw_uniform_argument"]):
                                data["previous_raw_uniform_argument"] = data["raw_uniform_argument"]
                                data["previous_uniform_magnitude"] = data["uniform_magnitude"]
                                data["uniform_argument"] = refineRawArgument(data["raw_uniform_argument"])
                                velocity_field.uniformFlow(data["uniform_magnitude"], data["uniform_argument"])                    
            else:
                for obj in non_uniform_interact:
                    obj.checkInteract(event)
                    if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                        if isinstance(obj, ui.ImageTitleButton):
                            if obj.getClicked():
                                data[obj.getIdentifier()] = obj.getValue()
                        else:
                            data[obj.getIdentifier()] = obj.getValue()
                        
                        if data["previous_non_uniform_flow_name"] != data["non_uniform_flow_name"]:
                            data["previous_non_uniform_flow_name"] = data["non_uniform_flow_name"]
                            velocity_field.nonUniformFlow(data["non_uniform_flow_name"])


    # Places visual elements
    for obj in tank_visual:
        obj.place()

        if data["flow"]:
            velocity_field.flow(data["dt"])
        else:
            velocity_field.stopFlow()
            
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
        else:
            for obj in non_uniform_visual:
                obj.place() 
    
    # Updates the screen with changes set in the loop
    pygame.display.flip()

    # Keeps the clock ticking
    data["frames"] = clock.get_fps()
    data["dt"] = clock.tick(FRAMES) / 1000
    
pygame.quit()