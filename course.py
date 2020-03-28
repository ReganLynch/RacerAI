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
        self.path = courses_folder + file_name
        self.display = display
        self.parse_lines_from_file()

    def draw(self):
        for line in self.lines:
            pygame.draw.line(self.display, self.line_color, line[0], line[1])

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
