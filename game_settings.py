import math
import os
import sys
 #hidding pygame welcome messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#make sure we find a display to output to
if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')
import numpy as np
from functools import partial
from tkinter import *
import pygame
from pygame_button import Button

#evolution settings / AI settings
population_size = 10
mutation_rate = 0.1  #how often they learn mutate
learning_factor = 0.8 #how much they deviate when they do learn
vision_distance = 3000  #how many pixels ahead the cars sensors can see

#folder settings
courses_folder = "courses/"
images_folder = "images/"

#game window dimentions
game_window_width = 1920
game_window_height = 1080
game_window_inset_x = 100
game_window_inset_y = 100

#Colour settings
game_background_colour = (49, 140, 49)
game_road_colour = (127, 133, 127)

#game window settings
FPS = 60

#the font used on th game page
display_font = 'Times New Roman'

#car settings
car_width = 20
car_height = 40
friction = 0.1
acceleration_factor = 1.0
max_speed = 5
rotation_factor = 3.5
