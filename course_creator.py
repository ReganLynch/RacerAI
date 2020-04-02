
import math
import sys
from tkinter import *
from game import intersects
from functools import partial
from game_settings import *
from course_shape_creator import *


#determines distance between two points
def get_dist(point1, point2):
    left = (point1[0] - point2[0])**2
    right = (point1[1] - point2[1])**2
    dist = math.sqrt(left + right)
    return math.floor(dist)

#helper method -> determines if point c is bewteen a and b (with a little bit of freedom)
def is_between(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    # compare versus epsilon for floating point values, or != 0 if using integers
    if get_dist(a, b) > 100:
        if abs(crossproduct) > 4000:
            return False
    else:
        if abs(crossproduct) > 1000:
            return False
    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
    if dotproduct < 0:
        return False
    squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False
    return True

#----------------------------------------------------
#click and hold to add line
#hover over and hit d or del to remove a line
#hit z to remove last line added
#hit s to save the track
class course_creator(object):

    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_window_inset_x,game_window_inset_x)
        self.gameDisplay = pygame.display.set_mode((game_window_width-200,game_window_height-200))
        self.clock = pygame.time.Clock()
        self.backround = game_road_colour
        self.creating_line = False
        self.hovered_on_end = False
        self.hover_pos = (0,0)
        self.start_pos = (0,0)
        self.end_pos = (0,0)
        self.line_color = (0,0,0)
        self.hover_color = (255,0,0)
        self.circle_col = (0,255,0)
        self.title_font = pygame.font.Font('freesansbold.ttf',20)
        self.sub_font = pygame.font.SysFont('Times New Roman',18)
        self.lines = []
        self.start_box = pygame.Rect(self.gameDisplay.get_width()/2 - car_width/2, self.gameDisplay.get_height()/2 - car_height/2, car_width, car_height)
        self.drawn_start_box  = False
        self.hovering_on_start = False
        self.points = {} #keep track of all pints (can have at most 2 lines ending at the same point)


    def run(self):
        stopped = False
        # game loop
        while not stopped:
            #set the backround
            self.gameDisplay.fill(self.backround)
            #put information in top left
            self.add_text_elements()
            #draw each of the lines
            for line in self.lines:
                pygame.draw.line(self.gameDisplay, self.line_color, line[0], line[1])
            #check click events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stopped = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:            #if user hits z -> remove last line
                        if len(self.lines) > 0:
                            self.points[''.join(map(str, self.lines[-1][0]))] -= 1
                            self.points[''.join(map(str, self.lines[-1][1]))] -= 1
                            self.lines.pop(len(self.lines) - 1)
                    if event.key == pygame.K_s:            #if user hits s -> save the lines into a file
                        self.save_window()
                    if event.key == pygame.K_t:            #if user hits t -> create a start position for the car
                        self.drawn_start_box = True
                #check for line creation
                self.check_create_line(event)
            #draw line being created
            if self.creating_line:
                pygame.draw.line(self.gameDisplay, self.line_color, self.start_pos, self.end_pos)

            if self.drawn_start_box:
                if self.start_box.collidepoint(pygame.mouse.get_pos()) or (self.hovering_on_start and pygame.mouse.get_pressed()[0]):
                    self.hovering_on_start = True
                    if pygame.mouse.get_pressed()[0]:
                        self.start_box.center = pygame.mouse.get_pos()
                else:
                    self.hovering_on_start = False
                self.draw_start_box()
            #check key events
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                stopped = True
                break
            #check for line deletion/hover events
            for line in self.lines:
                self.hovered_on_end = False
                self.hover_pos = (0,0)
                if is_between(line[0], line[1], pygame.mouse.get_pos()):                      #highliting line if hovered over
                    pygame.draw.aaline(self.gameDisplay, self.hover_color, line[0], line[1])
                    if keys[pygame.K_d] or keys[pygame.K_DELETE]:
                        self.points[''.join(map(str, line[0]))] -= 1
                        self.points[''.join(map(str, line[1]))] -= 1
                        self.lines.remove(line)
                if get_dist(pygame.mouse.get_pos(), line[0]) < 20:                      #drawine circle at end of lines
                    pygame.draw.circle(self.gameDisplay, self.circle_col, line[0], 5)
                    self.hovered_on_end = True
                    self.hover_pos = line[0]
                    break
                elif get_dist(pygame.mouse.get_pos(), line[1]) < 20:                    #drawine circle at end of lines
                    pygame.draw.circle(self.gameDisplay, self.circle_col, line[1], 5)
                    self.hovered_on_end = True
                    self.hover_pos = line[1]
                    break
            #redraw window
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()

    def add_text_elements(self):
        textSurface = self.title_font.render("Controls", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.005), top=(game_window_height * 0.01))
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("click and hold: creates a line", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.03))
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("d or del: deletes a line", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.045))
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("z: remove last line added", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.06))
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("s: save the course", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.075))
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("t: add start position", True, (255, 151, 5))
        rect = textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.09))
        self.gameDisplay.blit(textSurface, rect)

    #line creation
    def check_create_line(self, event):
        if self.hovering_on_start:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            #make sure that this line does not cross paths (intersect) with any other lines of the course
            line_intersects = False
            for course_line in self.lines:
                if self.start_pos != course_line[0] and self.start_pos != course_line[1] and self.end_pos != course_line[0] and self.end_pos != course_line[1]:
                    if intersects(course_line[0], course_line[1], self.start_pos, self.end_pos):
                        line_intersects = True
                        break
            #lines are only added if they are longer than 40, and does not intersect any other line of the course
            if get_dist(self.start_pos, self.end_pos) > 40 and not line_intersects:
                #check if points of the line are valid
                #when both endpoints are already in course
                if ''.join(map(str,self.start_pos)) in self.points and ''.join(map(str,self.end_pos)) in self.points:
                    if self.points[''.join(map(str,self.start_pos))] < 2 and self.points[''.join(map(str,self.end_pos))] < 2:
                        self.lines.append((self.start_pos, self.end_pos))
                        self.points[''.join(map(str,self.start_pos))] += 1
                        self.points[''.join(map(str,self.end_pos))] += 1
                #when only the start pos is in the course already
                elif ''.join(map(str,self.start_pos)) in self.points:
                    if self.points[''.join(map(str,self.start_pos))] < 2:
                        self.lines.append((self.start_pos, self.end_pos))
                        self.points[''.join(map(str,self.start_pos))] += 1
                        self.points[''.join(map(str,self.end_pos))] = 1
                #then only the end pos is already in the course
                elif ''.join(map(str,self.end_pos)) in self.points:
                    if self.points[''.join(map(str,self.end_pos))] < 2:
                        self.lines.append((self.start_pos, self.end_pos))
                        self.points[''.join(map(str,self.start_pos))] = 1
                        self.points[''.join(map(str,self.end_pos))] += 1
                #when neither the start point or the end point are part of the course already
                else:
                    self.lines.append((self.start_pos, self.end_pos))
                    self.points[''.join(map(str,self.start_pos))] = 1
                    self.points[''.join(map(str,self.end_pos))] = 1
            self.creating_line = False
        elif pygame.mouse.get_pressed()[0]:
            try:
                if not self.creating_line:
                    self.creating_line = True
                    if not self.hovered_on_end:
                        self.start_pos = event.pos
                    else:
                        self.start_pos = self.hover_pos
                    self.end_pos = event.pos
                else:
                    if not self.hovered_on_end:
                        self.end_pos = event.pos
                    else:
                        self.end_pos = self.hover_pos
            except AttributeError:
                pass

    #save course window
    def save_window(self):
        if not self.validate_course():
            return
        w = 350
        h = 80
        self.window = Tk()
        self.window.geometry('%dx%d+%d+%d' % (w, h, game_window_width/2 - w/2, game_window_height/2 - h/2))
        self.window.title("Save Course")
        lbl = Label(self.window, text="course name")
        lbl.place(relx=0.1, rely=0.2)
        e1 = Entry(self.window)
        e1.place(relx=0.4, rely=0.2)
        btn = Button(self.window, text='save', command=partial(self.save_course, e1))
        btn.config(height = 1, width = 10)
        btn.place(relx=0.35, rely=0.65)
        self.window.mainloop()

    #logic for saving the couse to local machine
    def save_course(self, entry):
        course_name = entry.get()
        self.window.destroy()
        file_name = courses_folder + course_name + ".txt"
        start_box_str = str(self.start_box.left) + "," + str(self.start_box.top) + "," + str(self.start_box.width) + "," + str(self.start_box.height) + "\n"
        try:
            with open(file_name, "w") as file:
                file.write(start_box_str)
                for line in self.lines:
                    line_str = str(line) + "\n"
                    file.write(line_str)
        except:
            os.mkdir(course_folder)
            with open(file_name, "w") as file:
                file.write(start_box_str)
                for line in self.lines:
                    line_str = str(line) + "\n"
                    file.write(line_str)
        #display to the user that the course was saved correctly
        self.window = Tk()
        w = 200
        h = 50
        self.window.geometry('%dx%d+%d+%d' % (w, h, game_window_width/2 - w/2, game_window_height/2 - h/2))
        self.window.title("Course Saved")
        lbl = Label(self.window, text='Course saved successfully.')
        lbl.place(relx=0.5, rely=0.3, anchor=CENTER)
        def close_window():
            self.window.destroy()
        btn = Button(self.window, text="Ok", bg="gray", fg="white", command=close_window)
        btn.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.window.lift()
        self.window.mainloop()

    def draw_start_box(self):
        if self.hovering_on_start:
            pygame.draw.rect(self.gameDisplay, (220, 154, 154), self.start_box)
            textSurface = self.sub_font.render("drag", True, self.line_color)
            rect = textSurface.get_rect()
            rect.center = (self.start_box.left + car_width/2, self.start_box.top + car_height/2)
            self.gameDisplay.blit(textSurface, rect)
        else:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), self.start_box)
            textSurface = self.sub_font.render("^", True, self.line_color)
            rect = textSurface.get_rect()
            rect.center = (self.start_box.left + car_width/2, self.start_box.top + car_height/8)
            self.gameDisplay.blit(textSurface, rect)
            textSurface = self.sub_font.render("|", True, self.line_color)
            rect = textSurface.get_rect()
            rect.center = (self.start_box.left + car_width/2, self.start_box.top + car_height/7)
            self.gameDisplay.blit(textSurface, rect)
            textSurface = self.sub_font.render("Start", True, self.line_color)
            rect = textSurface.get_rect()
            rect.center = (self.start_box.left + car_width/2, self.start_box.top + car_height/2)
            self.gameDisplay.blit(textSurface, rect)

    #validate the course
    def validate_course(self):
        valid_course = True
        err_msg = ''
        shapes = create_shapes_from_lines(self.lines)
        #check if there are enough shapes
        if len(shapes) < 2:
            valid_course = False
            err_msg = 'there are not enough line segements to \ncreate a course. Invalid Course.'
        #check if there are enough lines
        if len(self.lines) < 6:
            valid_course = False
            err_msg = 'not enough points to make a course, invalid course'
        #make sure all lines connect to another line
        #for this, for every point, there is another on the same spot
        pts = []
        for line in self.lines:
            pts.append(line[0])
            pts.append(line[1])
        pts.sort()
        for i in range(0, len(pts), 2):
            if pts[i] != pts[i+1]:
                #TODO Raise error
                err_msg = 'invalid course, there is a line segment that isnt closed'
                valid_course = False
        #check that the start position has been defined
        if not self.drawn_start_box:
            err_msg = 'no car start position defined, invalid course'
            valid_course = False
        #display error if the course was found to be invalid
        if not valid_course:
            self.window = Tk()
            w = 400
            h = 90
            self.window.geometry('%dx%d+%d+%d' % (w, h, game_window_width/2 - w/2, game_window_height/2 - h/2))
            self.window.title("Invalid Course")
            lbl = Label(self.window, text=err_msg)
            lbl.place(relx=0.5, rely=0.3, anchor=CENTER)
            def close_window():
                self.window.destroy()
            btn = Button(self.window, text="Ok", bg="gray", fg="white", command=close_window)
            btn.place(relx=0.5, rely=0.7, anchor=CENTER)
            self.window.lift()
            self.window.mainloop()
        return valid_course
