import pygame
from algorithms import tapping, typing
import interface as ui

pygame.init()

# Sets the constants of the screen surface
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1500
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
             "ui_active":True,
             "flow":False,
             "speed":0,
             "direction":"left"}


# Instantiates UI components
control_panel = ui.Window(screen, SCREEN_WIDTH-225, SCREEN_HEIGHT/2, 450, SCREEN_HEIGHT, ui_bg)
control_panel_title = ui.Label(screen, SCREEN_WIDTH-225, 30, "Control Panel", 30, ui_bg)
speed_label = ui.Label(screen, SCREEN_WIDTH-330, 120, "Speed:", 25, ui_bg)
speed_box = ui.Entry(screen, SCREEN_WIDTH-260, 120, 0, "speed", float, 27)
speed_unit_label = ui.Label(screen, SCREEN_WIDTH-115, 123,"ms\u207B\u00B9", 20, ui_bg)
direction_label = ui.Label(screen, SCREEN_WIDTH-330, 220, "Direction:", 20, ui_bg)
direction_dropdown = ui.Dropdown(screen, SCREEN_WIDTH-260, 219, ("Left", "Right", "Up", "Down"), "direction", str)

ui_objects = (control_panel, control_panel_title, speed_label, speed_box, speed_unit_label, direction_label, direction_dropdown)
ui_interactable = (speed_box, direction_dropdown)


# Instantiates tank components
flow_button = ui.Button(screen, 20, 25, "flow", "play_image.png", "pause_image.png", (0.1, 0.1), (0.1, 0.1), "space")

tank_objects = [flow_button,]
tank_interactable = [flow_button,]




running = True
while running:
    # Changes the caption of the window to view framerate and colours the screen blank, to allow for objects to be placed on it
    pygame.display.set_caption(f"Fluid Mechanics {clock.get_fps()}")
    screen.fill(bg_colour)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if typing(event):
            if keys[pygame.K_c]:
                variables["ui_active"] = toggleVariable(variables["ui_active"])

        if variables["tank"]:
            for obj in tank_interactable:
                obj.checkInteract(event, keys)
                if tapping(event) or typing(event):
                    variables[obj.getVariable()] = obj.getValue()


        if variables["ui_active"]:
            for obj in ui_interactable:
                obj.checkInteract(event)
                if tapping(event) or (typing(event) and event.unicode == "\x0D"):
                    variables[obj.getVariable()] = obj.getValue()


    # Places all objects, when relevant
    for obj in tank_objects:
        obj.place()

    if variables["ui_active"]:
        for obj in ui_objects:
            obj.place()


    # Updates the screen with changes that have been set in each loop
    pygame.display.flip()

    # Keeps loop in time with the clock
    dt = clock.tick(60) / 1000

pygame.quit()