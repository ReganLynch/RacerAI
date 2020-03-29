
#helper function for intersects
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

#determines line from AB intersects CD
def intersects(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


from game_settings import *
from car import car
from course import *
from threading import Thread
from genetic_algorithm import *

#prompts the user for what course they want to run
def get_course():
    file_name = { 'name' : ""}
    root = Tk()
    courses = get_all_saved_courses()
    w = 250
    h = 80
    root.title("Course Selection")
    root.geometry('%dx%d+%d+%d' % (w, h, game_window_width/2 - w/2, game_window_height/2 - h/2))
    tkvar = StringVar(root)
    tkvar.set("-- select one --") # set the default option
    popupMenu = OptionMenu(root, tkvar, *courses)
    popupMenu.place(relx=.5, rely=.7, anchor="c")
    lbl = Label(root, text="Choose a Course: ")
    lbl.place(relx=.5, rely=.3, anchor="c")
    #nested function
    def get_value(*args):
        val =  tkvar.get()
        root.destroy()
        file_name['name'] = val
    tkvar.trace('w', get_value)
    root.mainloop()
    return file_name['name']

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class game(object):

    def initialize_cars(self):
        for i in range(population_size):
            new_car = car(self.game_display, self.course.start_box.left, self.course.start_box.top, self.course.lines)
            self.cars.append(new_car)

    def __init__(self):
        pygame.init()
        f_name = get_course()
        if f_name == '':
            print("no course selected, exiting")
            quit()
        self.cars = []
        self.game_display = pygame.display.set_mode((game_window_width-200,game_window_height-200))
        pygame.display.set_caption("Tensorflow AI Racing Game")
        self.course = course(f_name, self.game_display)
        self.thread = Thread(target=self.initialize_cars(), args=())
        self.thread.start()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_window_inset_x, game_window_inset_y)
        self.clock = pygame.time.Clock()
        self.backround = (150,150,150)
        self.num_generations = 0


    def run(self):
        crashed = False
        self.thread.join()
        # game loop
        while not crashed:
            #set the backround
            self.game_display.fill(self.backround)
            #check if user exits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                    break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                crashed = True
                break
            #draw the course
            self.course.draw()
            #car thinking and drawing
            all_cars_crashed = True
            for car in self.cars:
                if not car.has_crashed:
                    all_cars_crashed = False
                    thought = car.think()
                    if thought[0] > 0.5:
                        car.rotate_left()
                    if thought[1] > 0.5:
                        car.rotate_right()
                    car.score += 1
                    car.accelerate()
                    car.check_crash()
                    car.draw()

            #check for new generation
            if all_cars_crashed:
                all_cars_crashed = False
                self.num_generations += 1
                self.cars = get_next_generation(self.cars)

            #redraw window
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
