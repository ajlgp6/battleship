# Includes function for dealing with sound effects

import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]

# Input passed to this function must be from a trusted source
def play_sound(file):
    file = os.path.join(main_dir, "assets/sound", f"{file}.wav")

    sound = pygame.mixer.Sound(file)
    sound.play()