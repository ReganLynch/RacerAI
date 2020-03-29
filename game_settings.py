import math
import os
 #hidding pygame welcome messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#make sure we find a display to output to
if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0')
import pygame
import numpy as np
#filter out all numpy warnings
np.warnings.filterwarnings("ignore")
from functools import partial
from tkinter import *

#evolution settings
population_size = 10
mutation_rate = 0.1
learning_factor = 0.5

#folder settings
courses_folder = "courses/"
images_folder = "images/"

#game window dimentions
game_window_width = 1920
game_window_height = 1080
game_window_inset_x = 100
game_window_inset_y = 100

#game window settings
FPS = 60

#car settings
car_width = 20
car_height = 40
friction = 0.1
acceleration_factor = 1.0
max_speed = 5
rotation_factor = 3.5

#AI settings
learning_rate = 0.1
vision_distance = 3000  #how many pixels in any direction the car can see
