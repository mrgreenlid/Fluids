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
pygame.display.set_icon(pygame.image.load("images\\ui\\icon_image.png"))


#Test data for initialisation
x, y = np.meshgrid(np.arange(-FIELD_WIDTH//2, FIELD_WIDTH//2), np.arange(FIELD_HEIGHT//2, -FIELD_HEIGHT//2, -1))
argand = x + 1j*y
positions = np.zeros((FIELD_HEIGHT, 2), dtype=np.int64)
velocities = np.zeros((FIELD_HEIGHT, FIELD_WIDTH), dtype=np.complex64)
sources = np.column_stack((np.full(shape=(FIELD_HEIGHT//10)-1, fill_value=FIELD_WIDTH-1, dtype=np.int64), np.arange(10, FIELD_HEIGHT, 10)))

# Initialises functions and algorithms
black = rgbToInt((0,0,0))
pygameToArgand(argand, 100, 200)
mapUniformFlow(argand, 1.0, 1.0)
mapParticles(pygame.surfarray.array2d(screen), positions, positions.astype(np.float64), velocities, sources, 10, 0.001, 1000, black, black)

# Cleans up test data
del x, y, argand, positions, velocities, sources, black


# Creates a clock to measure and regulate frames
clock = pygame.time.Clock()

data = {"flow":False,
        "control":True,
        "body_control":False,

             "particle":True,
             "streamline":False,
             "uniform":True,
             "previous_uniform_magnitude":1.0, 
             "uniform_magnitude":1.0,
             "uniform_argument_raw":"π",
             "previous_uniform_argument_raw":"π", 
             "uniform_argument":np.pi,
             "non_uniform_velocity_function":"",
             "frames":0.0,
             "dt":0.0}

control_box = ui.Box(screen, WIDTH-175, HEIGHT//2, 350, HEIGHT, UIBG, True)
control_title_label = ui.Label(screen, WIDTH-175, 30, "Control Panel", 40, bg=UIBG)
show_particle_label = ui.Label(screen, WIDTH-280, 100, "Particles:", 22, bg=UIBG)
particle_field_radiobutton = ui.RadioButton(screen, WIDTH-90, 100, 0, 50, "particle")
show_field_label = ui.Label(screen, WIDTH-270, 150, "Vector field:", 22, bg=UIBG)

streamline_label = ui.Label(screen, WIDTH-270, 200, "Streamline:", 22, bg=UIBG)
streamline_checkbox = ui.Checkbox(screen, WIDTH-90, 200, "streamline" )

uniform_label = ui.Label(screen, WIDTH-280, 250, "Uniform:", 22, bg=UIBG)
non_uniform_label = ui.Label(screen, WIDTH-130, 250, "Non-Uniform:", 22, bg=UIBG )
uniform_radiobutton = ui.RadioButton(screen, WIDTH-220, 250, 175, 0, "uniform")

function_divider = ui.Box(screen, WIDTH-175, 290, 300, 1)

uniform_magnitude_label = ui.Label(screen, WIDTH-268, 330, "Magnitude:", 22, bg=UIBG)
uniform_magnitude_entry = ui.Entry(screen, WIDTH-175, 330, "uniform_magnitude", data["uniform_magnitude"], max_length=6, font="Courier")
uniform_argument_label = ui.Label(screen, WIDTH-290, 380, "Angle:", 22, bg=UIBG)
uniform_argument_composite_entry = ui.CompositeEntry(screen, WIDTH-175, 380, "uniform_argument_raw", data["uniform_argument_raw"], 25, ("π", "e"), ((100, 35), (130, 35)), (20,20), 25, button_font="Courier", max_length=9,  dtype=str, font="Courier")

velocity_funtion_label = ui.Label(screen, WIDTH-230, 458, "Velocity function:", 25, bg=UIBG)

uniform_magnitude_datalabel = ui.DataLabel(screen, WIDTH-194, 534, "uniform_magnitude", data["uniform_magnitude"], 30, 6, True, "left", bg=UIBG, font="Courier")
times_label = ui.Label(screen, WIDTH-195, 534, "\u00D7", 30,  bg=UIBG, font="Courier")
e_label = ui.Label(screen, WIDTH-175, 530, "e", 36, bg=UIBG, font="Courier")
i_label = ui.Label(screen, WIDTH-159, 515, "i", 22, bg=UIBG, font="SWital")
open_bracket_label = ui.Label(screen, WIDTH-148, 515, "(", 30, bg=UIBG, font="Courier")
uniform_argument_datalabel = ui.DataLabel(screen, WIDTH-135, 515, "uniform_argument", data["uniform_argument"], 21, max_length=6, bg=UIBG, font="Courier")
close_bracket_label = ui.Label(screen, WIDTH-55, 515, ")", 30, bg=UIBG, font="Courier")

flow_button = ui.DualImageBooleanButton(screen, WIDTH-175, 650, "flow", "images\\ui\\play_image.png", "images\\ui\\pause_image.png", 0.2, 0.2)
data_divider = ui.Box(screen, WIDTH-175, 700, 300, 1)
frames_label = ui.Label(screen, WIDTH-250, 730, "Performance (fps):", bg=UIBG)
frames_datalabel = ui.DataLabel(screen, WIDTH-100, 730, "frames", data["frames"], max_length=8, bg=UIBG)

control_visual = (control_box, control_title_label, 
                  show_field_label, particle_field_radiobutton, show_particle_label,
                  streamline_label, streamline_checkbox, 
                  uniform_label, uniform_radiobutton, non_uniform_label,
                  function_divider,
                  
                  flow_button, data_divider, frames_label, frames_datalabel)

uniform_visual = (velocity_funtion_label, uniform_magnitude_label, uniform_magnitude_entry, 
                  uniform_argument_label, uniform_argument_composite_entry,
                  uniform_magnitude_datalabel,times_label,  e_label, i_label, open_bracket_label,  uniform_argument_datalabel, close_bracket_label)

control_interact = (particle_field_radiobutton, 
                    streamline_checkbox,
                    uniform_radiobutton, 
                    flow_button)

uniform_interact = (uniform_magnitude_entry, 
                    uniform_argument_composite_entry)


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
                    
                        if data["previous_uniform_argument_raw"] != data["uniform_argument_raw"] or data["previous_uniform_magnitude"] != data["uniform_magnitude"]:
                            data["previous_uniform_magnitude"] = data["uniform_magnitude"]
                            if validAngleExpression(data["uniform_argument_raw"]):
                                data["previous_uniform_argument_raw"] = data["uniform_argument_raw"]
                                data["uniform_argument"] = refineRawArgument(data["uniform_argument_raw"])
                                velocity_field.uniformFlow(data["uniform_magnitude"], data["uniform_argument"])
                                    
            else:
                velocity_field.nonUniformFlow(data["non_uniform_velocity_function"])


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
    
    # Updates the screen with changes set in the loop
    pygame.display.flip()

    # Keeps the clock ticking
    data["frames"] = clock.get_fps()
    data["dt"] = clock.tick(FRAMES) / 1000



pygame.quit()