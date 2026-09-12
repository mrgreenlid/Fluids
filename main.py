import pygame
import interface as ui
from algorithms import *
import fluid as fluid

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

             "speed":1.0,
             "field":True,
             "streamline":False,
             "scenario":"tunnel",
             "frames":0.0}


control_box = ui.Box(screen, WIDTH-175, HEIGHT//2, 350, HEIGHT, UIBG, True)
control_title_label = ui.Label(screen, WIDTH-175, 30, "Control Panel", 40, bg=UIBG)
speed_label = ui.Label(screen, WIDTH-290, 100, "Speed:", 22, bg=UIBG)
speed_entry = ui.Entry(screen, WIDTH-220, 100, "speed", data["speed"], font="Courier")
speed_unit_label = ui.Label(screen, WIDTH-45, 100, "ms\u207B\u00B9", bg=UIBG)
show_field_label = ui.Label(screen, WIDTH-270, 150, "Vector field:", 22, bg=UIBG)
field_particle_radiobutton = ui.RadioButton(screen, WIDTH-90, 150, 0, 50, "field")
show_particle_label = ui.Label(screen, WIDTH-280, 200, "Particles:", 22, bg=UIBG)
streamline_label = ui.Label(screen, WIDTH-270, 250, "Streamline:", 22, bg=UIBG)
streamline_checkbox = ui.Checkbox(screen, WIDTH-90, 250, "streamline" )
scenario_label = ui.Label(screen, WIDTH-277, 300, "Scenario:", 22, bg=UIBG)
scenario_dropdown = ui.Dropdown(screen, WIDTH-220, 300, "scenario", ("Tunnel", "Falling", "Vortex", "Custom"), dtype=str, font="Courier")


flow_button = ui.DualImageBooleanButton(screen, WIDTH-175, 600, "flow", "images\\ui\\play_image.png", "images\\ui\\pause_image.png", 0.2, 0.2)
control_divider = ui.Box(screen, WIDTH-175, 650, 300, 1)
frames_label = ui.Label(screen, WIDTH-250, 680, "Performance (fps):", bg=UIBG)
frames_datalabel = ui.DataLabel(screen, WIDTH-100, 680, "frames", data["frames"], bg=UIBG)

control_visual = (control_box, control_title_label, speed_label, speed_entry, speed_unit_label,
                  show_field_label, field_particle_radiobutton, show_particle_label,
                  streamline_label, streamline_checkbox, scenario_label,
                  scenario_dropdown,
                  flow_button, control_divider, frames_label, frames_datalabel)

control_interact = (speed_entry, field_particle_radiobutton, streamline_checkbox, scenario_dropdown,
                    flow_button)


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
                        

    # Places visual elements
    for obj in tank_visual:
        obj.place()

    if data["control"]:
        for obj in control_visual:
            if isinstance(obj, ui.DataLabel):
                obj.update(data[obj.getIdentifier()])
            obj.place()



    # Updates the screen with changes set in the loop
    pygame.display.flip()

    # Keeps the clock ticking
    data["frames"] = clock.get_fps()
    clock.tick(FRAMES) 



pygame.quit()