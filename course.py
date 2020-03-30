from os import listdir
from game_settings import *

#returns a list of files that are courses
def get_all_saved_courses():
    return listdir(courses_folder)

#defines a course object
class course(object):

    def __init__(self, file_name, display):
        self.lines = []
        self.start_box = pygame.Rect(0,0,0,0)
        self.line_color = (0,0,0)
        if not file_name == '':
            self.path = courses_folder + file_name
        else:
            print("no course selected, exiting")
            quit()
        self.display = display
        self.parse_lines_from_file()
        self.get_connected_lines()

    def draw(self):
        #for line in self.lines:
            #pygame.draw.line(self.display, self.line_color, line[0], line[1])
        r = 0
        for shape in self.all_shapes:
            for line in shape:
                pygame.draw.line(self.display, (0, r, 0), line[0], line[1])
            r += 50

    def get_connected_lines(self):
        lines_copy = self.lines.copy()
        self.all_shapes = []
        while len(lines_copy) > 0:
            curr_shape = []
            curr_shape.append(lines_copy.pop(0))
            i = 0
            #go through all lines that havent been processed yet
            while i < len(lines_copy):
                curr_line = lines_copy[i]
                found_line = False
                #check if the current line connects to any of the lines in the current SHAPE
                for shape_line in curr_shape:
                    if shape_line[0] == curr_line[1]:
                        curr_shape.append(curr_line)
                        lines_copy.remove(curr_line)
                        found_line = True
                        break
                    if shape_line[0] == curr_line[0]:
                        curr_shape.append(curr_line)
                        lines_copy.remove(curr_line)
                        found_line = True
                        break
                    if shape_line[1] == curr_line[0]:
                        curr_shape.append(curr_line)
                        lines_copy.remove(curr_line)
                        found_line = True
                        break
                    if shape_line[1] == curr_line[1]:
                        curr_shape.append(curr_line)
                        lines_copy.remove(curr_line)
                        found_line = True
                        break
                if found_line:
                    i = 0
                else:
                    i += 1
            #append the current shape to all shapes
            self.all_shapes.append(curr_shape)

    def parse_lines_from_file(self):
        first = True
        with open(self.path) as file:
            for curr_line in file:
                if first:
                    first = False
                    split = curr_line.split(',')
                    self.start_box.left = int(split[0])
                    self.start_box.top = int(split[1])
                    self.start_box.width = int(split[2])
                    self.start_box.height = int(split[3])
                else:
                    split = curr_line.split(',')
                    index = -1
                    for word in split:
                        index += 1
                        word = word.replace('(', '')
                        word = word.replace(')', '')
                        word = word.replace(' ', '')
                        word = word.replace('\n', '')
                        split[index] = int(word)
                    pt1 = (split[0], split[1])
                    pt2 = (split[2], split[3])
                    self.lines.append((pt1,pt2))
