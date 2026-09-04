import pygame
import interface as ui
import fluid as fluid
from algorithms import *
import databaseManagement as db
from os.path import isfile


# Initialises database tables
if not isfile("fluids.db"):
    db.initialiseVelocityFunctionTable()
    db.initialiseBodyTable()

# JIT Compiles subroutines to be used later on
translate(rotate(np.array([(1.0, 0), (1.0, 1.0),(1.0, -1.0)]),np.pi), 0, 0)
colourByMagnitude(0.0)

pygame.init()

# Sets constants of the screen
HEIGHT = 800
WIDTH = 1600
FRAMES = 60
BG = "#FFFFFF"
UIBG = "#ECECEC"

MAX_PARTICLES = 5000

# Creates the pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG)
pygame.display.flip()
pygame.display.set_icon(pygame.image.load("images\\ui\\icon_image.png"))

# Creates a clock to measure and regulate frames
clock = pygame.time.Clock()

# Stores variables to be used across the program
data = {"show_tank":True,
        "show_control":True,
        "show_body":False,
        "show_field":True,
        "body_index":0,
        "clear_body":False,
        "field_rows":16,
        "particle_count":100,
        "show_streamline":False,
        "flow":False,
        "q": "",
        

        "speed":1.0,
        "scenario":"falling",
        "circulation":0.0,
        "flux":0.0,
        "ke":0.0,
        "frames":0}


# Creates control panel components
control_panel_box = ui.Box(screen, WIDTH-175, HEIGHT//2, 350, HEIGHT, UIBG, True)
control_panel_title_label = ui.Label(screen, WIDTH-175, 30, "Control Panel", 30, bg=UIBG)
speed_box_label = ui.Label(screen, WIDTH-285, 100, "Speed:", bg=UIBG)
speed_box_entry = ui.Entry(screen, WIDTH-200, 100, data["speed"], "speed", max_length=8, dtype=float) 
speed_box_units_label = ui.Label(screen, WIDTH-50, 100, "ms\u207B\u00B9", bg=UIBG)
show_field_box_label = ui.Label(screen, WIDTH-248, 150, "Vector field:", bg=UIBG)
field_rows_increment = ui.Increment(screen, WIDTH-60, 150, 30, 0 , "field_rows", data["field_rows"], 30, 2)
particle_count_increment = ui.Increment(screen, WIDTH-60, 200, 30, 0 , "particle_count", data["particle_count"], MAX_PARTICLES, 100)
show_field_box_radiobutton = ui.RadioButton(screen, WIDTH-100, 150, 0, 50, "show_field")
not_show_field_box_label = ui.Label(screen, WIDTH-263, 200, "Particles:", bg=UIBG)
streamline_box_label = ui.Label(screen, WIDTH-258, 250, "Streamline:", bg=UIBG)
streamline_box_checkbox = ui.Checkbox(screen, WIDTH-100, 250, "show_streamline")
scenario_label = ui.Label(screen, WIDTH-270, 300, "Scenario:", bg=UIBG)
scenario_dropdown = ui.Dropdown(screen, WIDTH-200, 300, ("Tunnel", "Falling", "Vortex", "Custom"), "scenario", dtype=str)

custom_scenario_box_label = ui.Label(screen, WIDTH-283, 350, "Custom:", bg=UIBG) 
custom_scenario_box_entry = ui.Entry(screen, WIDTH-230, 350, data["q"], "q", 14, 220, str)

select_body_button = ui.ImageBooleanButton(screen, WIDTH-175, 450, "show_body", "images\\ui\\select_body.png", 0.5)

control_panel_data_divider_box = ui.Box(screen, WIDTH-175, 600, 240, 1, "#000000")

circulation_data_label = ui.Label(screen, WIDTH-250, 630, "Circulation:", 17, bg=UIBG, font="Courier")
circulation_data_datalabel = ui.DataLabel(screen, WIDTH-110, 630, data["circulation"], "circulation", 17, bg=UIBG, font="Courier")
flux_data_label = ui.Label(screen, WIDTH-285, 660, "Flux:", 17, bg=UIBG, font="Courier")
flux_data_datalabel = ui.DataLabel(screen, WIDTH-110, 660, data["flux"], "flux", 17, bg=UIBG, font="Courier")
ke_data_label = ui.Label(screen, WIDTH-257, 690, "Obj KE (J):", 17, bg=UIBG, font="Courier")
ke_data_datalabel = ui.DataLabel(screen, WIDTH-110, 690, data["ke"], "ke", 17, bg=UIBG, font="Courier")
frames_data_label = ui.Label(screen, WIDTH-222, 720, "Performance (fps):", 17, bg=UIBG, font="Courier")
frames_data_datalabel = ui.DataLabel(screen, WIDTH-110, 720, data["frames"], "frames", 17, bg=UIBG, font="Courier")

control_visual = (control_panel_title_label, speed_box_label, 
                    speed_box_entry, speed_box_units_label, show_field_box_label,
                    field_rows_increment, particle_count_increment,
                    show_field_box_radiobutton, not_show_field_box_label,
                    streamline_box_label, streamline_box_checkbox, scenario_label,scenario_dropdown,
                    select_body_button, control_panel_data_divider_box, circulation_data_label, 
                    circulation_data_datalabel, flux_data_label, flux_data_datalabel, ke_data_label, 
                    ke_data_datalabel, frames_data_label, frames_data_datalabel)

control_interact = (speed_box_entry, field_rows_increment, particle_count_increment, show_field_box_radiobutton,
                    streamline_box_checkbox, scenario_dropdown, select_body_button)

custom_visual = (custom_scenario_box_label, custom_scenario_box_entry)
custom_interact = (custom_scenario_box_entry, )



# Creates body selection components
body_selection_title_label = ui.Label(screen, WIDTH-175, 30, "Select Object", 30, bg=UIBG)
back_from_body_button = ui.ImageBooleanButton(screen, WIDTH-320, 28, "show_control", "images\\ui\\back_from_body.png", 0.15)
clear_body_button = ui.ImageBooleanButton(screen, WIDTH-175, 700, "clear_body", "images\\ui\\clear_body.png", 0.6)
body_select_1 = ui.BodySelectionButton(screen, WIDTH-250, 120, 1, 0.2)
body_select_2 = ui.BodySelectionButton(screen, WIDTH-95, 120, 2, 0.3)
body_select_3 = ui.BodySelectionButton(screen, WIDTH-250, 320, 3, 0.3)
body_select_4 = ui.BodySelectionButton(screen, WIDTH-95, 320, 4, 0.2)
body_select_5 = ui.BodySelectionButton(screen, WIDTH-250, 520, 5, 0.18)
body_select_6 = ui.BodySelectionButton(screen, WIDTH-95, 520, 6, 0.3)


body_visual = (body_selection_title_label, back_from_body_button, body_select_1, body_select_2, 
                body_select_3, body_select_4, body_select_5, body_select_6, clear_body_button)

body_interact = (back_from_body_button, body_select_1, body_select_2, body_select_3, body_select_4, 
                body_select_5, body_select_6, clear_body_button)


# Creates tank components
flow_button = ui.DualImageBooleanButton(screen, 22, 30, "flow", "images\\ui\\play_image.png", "images\\ui\\pause_image.png", 0.2, 0.2)
vector_field = fluid.VectorField(screen, data["show_field"], data["field_rows"], data["flow"])

tank_visual = (vector_field, flow_button,)
tank_interact = (flow_button,)



body = fluid.Body(screen)
vector_field.linkBody(body)

source = fluid.Source(screen)
source.linkVectorField(vector_field)

particles = pygame.sprite.Group()

for _ in range(MAX_PARTICLES):
    particles.add(fluid.Particle(screen, vector_field, source))



vector_field.updateFunction(db.searchVelocityFunction(data["scenario"]))

# Creates event loop for the main program
running = True
while running:
    pygame.display.set_caption("Fluid Mechanics NEA")
    screen.fill(BG)

    # 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        # Checks and acts on keybind presses
        if typing(event):
                if keys[pygame.K_c]:
                    data["show_control"] = not data["show_control"]
                    data["show_body"] = False
                
        # Checks for interaction with tank interactables
        if data["show_tank"]:
            for obj in tank_interact:
                if isinstance(obj, Input):
                        obj.checkInteract(event)
                else:
                    obj.checkInteract()
                if tapping(event) or typing(event):
                    data[obj.getVariable()] = obj.getValue()


            # Checks for interaction with the body
            if data["body_index"] != 0:
                body.checkInteract(event)

            # Checks for interaction with the source
            if data["flow"] and not data["show_field"]:
                if tapping(event):
                    source.update()


            # Checks for interaction with control interactables
            if data["show_control"]:
                for obj in control_interact:
                    if isinstance(obj, Input):
                        obj.checkInteract(event)
                    else:
                        obj.checkInteract()
                    if tapping(event) or (typing(event) and event.type == pygame.KEYDOWN and event.unicode == "\x0D"):
                        data[obj.getVariable()] = obj.getValue()
                        if data["scenario"] != "custom" :
                            vector_field.updateFunction(db.searchVelocityFunction(data["scenario"]))


                # Checks for interaction with custom interactables
                if data["scenario"] == "custom":
                    for obj in custom_interact:
                        obj.checkInteract(event)
                        if tapping(event) or (typing(event) and event.type == pygame.KEYDOWN and event.unicode == "\x0D"):
                            data[obj.getVariable()] = obj.getValue()
                            if validVelocityFunction(data["q"]):
                                if not db.searchVelocityFunction(data["q"]):
                                    db.saveVelocityFunction(data["q"])
                                vector_field.updateFunction(db.searchVelocityFunction(data["q"]))


            # Checks for interaction with body selection interactables
            if data["show_body"]:
                for obj in body_interact:
                    if isinstance(obj, Input):
                        obj.checkInteract(event)
                    else:
                        obj.checkInteract()
                    if tapping(event) or (typing(event) and event.type == pygame.KEYDOWN and event.unicode == "\x0D"):
                        if isinstance(obj, ui.BodySelectionButton):
                            if obj.getClickFlag():
                                data[obj.getVariable()] = obj.getValue()
                        else:
                            data[obj.getVariable()] = obj.getValue()


    # Places visual elements of tank
    if data["show_tank"]:
        for obj in tank_visual:
            if isinstance(obj, fluid.VectorField):
                obj.update(*[data[variable] for variable in obj.getVariable()])
            obj.place()

        # Places particles as they flow
        if data["flow"] and not data["show_field"]:
            particles.update()
           
            


        # Places the body
        body.update(data["body_index"], data["show_streamline"])
        body.place()
        
        ### TODO Make logic for updating vector field for object


        # Places visual elements of control panel 
        if data["show_control"]:
            data["show_body"] = False
            control_panel_box.place()

            # Places visual elements of custom scenario changer
            if data["scenario"] == "custom":
                for obj in custom_visual:
                    obj.place()

            for obj in control_visual:
                if isinstance(obj, Output):
                    obj.update(data[obj.getVariable()])
                obj.place()
            

        # Places visual elements of body selection
        if data["show_body"]:
            data["show_control"] = False

            # Checks if the tank needs clearing of a body
            if data["clear_body"]:
                data["body_index"] = 0
                data["clear_body"] = False

            control_panel_box.place()
            for obj in body_visual:
                obj.place()

    # Updates the screen with changes set in the loop
    pygame.display.flip()

    # Keeps the clock ticking
    data["frames"] = clock.get_fps()
    clock.tick(FRAMES) 



pygame.quit()

