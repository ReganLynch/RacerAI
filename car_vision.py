from car import *
import math
from game import intersects
from game_settings import *


def calculate_mid_point(pt1, pt2):
    return ((pt1[0] + pt2[0])/2, (pt1[1] + pt2[1])/2)

def calculate_slope_of_bisector(pt1, pt2):
    return ((pt2[0] - pt1[0]), (pt2[1] - pt1[1]))

def calculate_new_point(start_pt, slope, pt_distance ,view_distance):
    new_x = (start_pt[0] + (slope[1] / pt_distance) * view_distance)
    new_y = (start_pt[1] + (slope[0] / pt_distance) * -view_distance)
    return (new_x, new_y)

def calculate_new_vision_line(pt1, pt2, distance):
    vision_start = calculate_mid_point(pt1, pt2)
    rise_run = calculate_slope_of_bisector(pt1, pt2)
    pt_distance = math.sqrt( ((pt2[0] - pt1[0])**2) + ((pt2[1] - pt1[1])**2) )
    vision_end = calculate_new_point(vision_start, rise_run, pt_distance,distance)
    return (vision_start, vision_end)

def get_intersection_point(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)



##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
class car_vision(object):

    def __init__(self, box_points, course_lines):
        self.front_left = box_points[0]
        self.front_right = box_points[1]
        self.back_left = box_points[2]
        self.back_right = box_points[3]
        self.course_lines = course_lines
        self.calculate_vision_lines()
        self.find_vision_boundries()

    def update(self, box_points):
        self.front_left = box_points[0]
        self.front_right = box_points[1]
        self.back_left = box_points[2]
        self.back_right = box_points[3]
        self.calculate_vision_lines()
        self.find_vision_boundries()

    # calculates all vision lines
    def calculate_vision_lines(self):
        self.vision_lines = []
        front_vision_line = calculate_new_vision_line(self.front_left, self.front_right, vision_distance)
        self.vision_lines.append(front_vision_line)
        left_vision_line = calculate_new_vision_line(self.back_left, self.front_left, vision_distance)
        self.vision_lines.append(left_vision_line)
        right_vision_line = calculate_new_vision_line(self.front_right, self.back_right, vision_distance)
        self.vision_lines.append(right_vision_line)
        mid_left = calculate_mid_point(self.front_left, self.back_left)
        mid_right = calculate_mid_point(self.front_right, self.back_right)
        left_diag = calculate_new_vision_line(mid_left, self.front_right, vision_distance)
        self.vision_lines.append((self.front_left, left_diag[1]))
        right_diag = calculate_new_vision_line(self.front_left, mid_right, vision_distance)
        self.vision_lines.append((self.front_right, right_diag[1]))

    # find where the vision lines hit a wall
    def find_vision_boundries(self):
        for i in range(len(self.vision_lines)):
            for course_line in self.course_lines:
                if intersects(self.vision_lines[i][0], self.vision_lines[i][1], course_line[0], course_line[1]):
                    intersection = get_intersection_point(self.vision_lines[i], course_line)
                    self.vision_lines[i] = (self.vision_lines[i][0], intersection)
        self.vision_distances = []
        for line in self.vision_lines:
            line_length = math.sqrt( ((line[1][0] - line[0][0])**2) + ((line[1][1] - line[0][1])**2) )
            self.vision_distances.append(line_length)
