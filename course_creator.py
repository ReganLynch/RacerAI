
import math
import sys
from tkinter import *
from functools import partial
from game_settings import *


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
        self.backround = (150,150,150)
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
                            del self.lines[-1]
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
        textSurface = self.title_font.render("Controls", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (50, 20)
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("click and hold: creates a line", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (140, 50)
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("d or del: deletes a line", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (120, 70)
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("z: remove last line added", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (130, 90)
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("s: save the course", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (105, 110)
        self.gameDisplay.blit(textSurface, rect)
        textSurface = self.sub_font.render("t: add start position", True, self.line_color)
        rect = textSurface.get_rect()
        rect.center = (115, 130)
        self.gameDisplay.blit(textSurface, rect)

    #line creation
    def check_create_line(self, event):
        if self.hovering_on_start:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            if get_dist(self.start_pos, self.end_pos) > 40:             #lines are only added if they are longer than 40
                self.lines.append((self.start_pos, self.end_pos))
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
        w = 250
        h = 80
        self.window = Tk()
        self.window.geometry('%dx%d+%d+%d' % (w, h, game_window_width/2 - w/2, game_window_height/2 - h/2))
        self.window.title("Save Course")
        lbl = Label(self.window, text="course name")
        lbl.place(x=20, y=10)
        e1 = Entry(self.window)
        e1.place(x=100, y=10)
        btn = Button(self.window, text='save', command=partial(self.save_course, e1))
        btn.config(height = 1, width = 10)
        btn.place(x=w/3, y=40)
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
