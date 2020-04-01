from os import listdir
from game_settings import *
from course_shape_creator import *

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
        self.all_shapes = create_shapes_from_lines(self.lines)
        areas = sort_shapes_by_area(self.all_shapes)
        self.max_shape_index = areas.index(max(areas))

        for area in areas:
            print(area)
        print(self.max_shape_index)

    def draw(self):
        pygame.draw.polygon(self.display, game_road_colour, self.all_shapes[self.max_shape_index])
        for i in range(0, len(self.all_shapes)):
            if i != self.max_shape_index:
                pygame.draw.polygon(self.display, game_background_colour, self.all_shapes[i])


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
