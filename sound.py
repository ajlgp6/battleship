##Includes function for dealing with sound effects

import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file):
    ##Loads a sound file into a Sound object
    file = os.path.join(main_dir, "data", file)

    sound = pygame.mixer.Sound(file)
    return sound