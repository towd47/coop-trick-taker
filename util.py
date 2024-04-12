import os
import json
import pygame

def create_keybinds():
    keybinds = {
        "controls":{
            "0":{"Step": pygame.K_SPACE, "Back": pygame.K_ESCAPE, "Accelerate": pygame.K_f},
            "1":{"Step": pygame.K_SPACE, "Back": pygame.K_ESCAPE, "Accelerate": pygame.K_f}
        },
        "current_profile": 0
    }
    return keybinds

def load_existing_keybinds(keybind_file):
    with open(os.path.join(keybind_file), 'r+') as file:
        controls = json.load(file)
    return controls

def load_keybinds():
    try:
        keybinds = load_existing_keybinds("keybinds.json")
    except:
        keybinds = create_keybinds()
        save_keybinds(keybinds)

    return keybinds

def save_keybinds(keybinds):
    with open(os.path.join(os.getcwd(), 'keybinds.json'), 'w') as file:
        json.dump(keybinds, file)