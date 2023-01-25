
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
# TODO: FIX CONSOLE ERRORS -> caused by tkinter
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

def return_to_splash_screen():
    from GameRunner import show_splash_screen
    pygame.quit()
    show_splash_screen()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# TODO: add button to save the car

class game(object):

    SPLASH_SCREEN_BUTTON_STYLE = {
        "hover_color": (0,255,0),
        "clicked_color": (0,255,0),
        "clicked_font_color": (0,0,0),
        "hover_font_color": (0,0,0),
        "text": "Return Home"
    }

    DRAW_VISION_BUTTON_STLE = {
        "hover_color": (255,255,255),
        "clicked_color": (0,255,0),
        "clicked_font_color": (0,0,0),
        "hover_font_color": (0,0,0),
        "text": "Display Car Vision"
    }

    HIDE_VISION_BUTTON_STLE = {
        "hover_color": (255,255,255),
        "clicked_color": (0,255,0),
        "clicked_font_color": (0,0,0),
        "hover_font_color": (0,0,0),
        "text": "Hide Car Vision"
    }

    #hide
    #inactiveColour=(220,0,0), hoverColour=(255,255,255),pressedColor=(0,255,0)
    #show
    #inactiveColour=(207, 188, 19), hoverColour=(255,255,255),pressedColor=(0,255,0)

    def initialize_cars(self):
        for i in range(population_size):
            new_car = car(self.game_display, self.course.start_box.left, self.course.start_box.top, self.course.lines)
            self.cars.append(new_car)

    def draw_vision_lines(self):
        self.draw_car_vision = not self.draw_car_vision
        #TODO FIX
        if self.draw_car_vision:
            self.draw_vision_button = Button(
                                    (int(game_window_width * 0.02), int(game_window_height * 0.11), int(game_window_width * 0.07), int(game_window_height * 0.03)),
                                    (220,0,0),
                                    self.draw_vision_lines, 
                                    **self.HIDE_VISION_BUTTON_STLE)
        else:
            self.draw_vision_button = Button(
                                    (int(game_window_width * 0.02), int(game_window_height * 0.11), int(game_window_width * 0.07), int(game_window_height * 0.03)),
                                    (207, 188, 19),
                                    self.draw_vision_lines, 
                                    **self.DRAW_VISION_BUTTON_STLE)

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
        self.initialize_cars()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_window_inset_x, game_window_inset_y)
        self.clock = pygame.time.Clock()
        self.backround = game_background_colour
        self.font = pygame.font.SysFont(display_font,14)
        self.num_generations = 1
        self.curr_max_score = 0
        self.max_score_all_generations = 0
        self.draw_car_vision = False

        #TODO fix
        self.splash_screen_btn = Button(
                                (int(game_window_width * 0.8), int(game_window_height * 0.75), int(game_window_width * 0.06), int(game_window_height * 0.03)),
                                (0,200,50),
                                return_to_splash_screen, 
                                **self.SPLASH_SCREEN_BUTTON_STYLE)
        
        self.draw_vision_button = Button(
                                (int(game_window_width * 0.02), int(game_window_height * 0.11), int(game_window_width * 0.07), int(game_window_height * 0.03)),
                                (207, 188, 19),
                                self.draw_vision_lines, 
                                **self.DRAW_VISION_BUTTON_STLE)

    def display_evolution_info(self):
        #display generation information
        gen_textSurface = self.font.render("Generation: " + str(self.num_generations), True, (0, 0, 0))
        rect = gen_textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.02))
        self.game_display.blit(gen_textSurface, rect)
        #display current max score information
        curr_score_textSurface = self.font.render("Current Max Score: " + str(self.curr_max_score), True, (0, 0, 0))
        rect = curr_score_textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.06))
        self.game_display.blit(curr_score_textSurface, rect)
        #display the overall max score information
        overall_score_textSurface = self.font.render("Overall Max Score: " + str(self.max_score_all_generations), True, (0, 0, 0))
        rect = overall_score_textSurface.get_rect(left=(game_window_width * 0.02), top=(game_window_height * 0.08))
        self.game_display.blit(overall_score_textSurface, rect)

    def run(self):
        crashed = False
        # game loop
        while not crashed:
            #set the backround
            self.game_display.fill(self.backround)
            #check if user exits
            game_events = pygame.event.get()
            for event in game_events:
                if event.type == pygame.QUIT:
                    crashed = True
                    break
                #check the events of the return to splash screen button
                self.splash_screen_btn.check_event(event)
                #check events for draw vision lines button
                self.draw_vision_button.check_event(event)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                crashed = True
                break
            #draw the course
            self.course.draw()
            #draw the generation info
            self.display_evolution_info()
            #car thinking and drawing
            all_cars_crashed = True
            self.curr_max_score = 0
            for car in self.cars:
                if not car.has_crashed:
                    all_cars_crashed = False
                    #have neurat net predict move
                    thought = car.think()
                    if thought[0] > 0.5:
                        car.rotate_left()
                    if thought[1] > 0.5:
                        car.rotate_right()
                    #increment car score
                    car.score += 1
                    #keep track of the highest score
                    if car.score > self.curr_max_score:
                        self.curr_max_score = car.score
                    #perfom car actions
                    car.accelerate()
                    car.check_crash()
            #update the max score across all generations
            if self.curr_max_score > self.max_score_all_generations:
                self.max_score_all_generations = self.curr_max_score
            #check for new generation
            if all_cars_crashed:
                all_cars_crashed = False
                self.num_generations += 1
                self.cars = get_next_generation(self.cars)
            #only after the speed loop do we draw each car
            for car in self.cars:
                car.draw(self.draw_car_vision)
            #redraw the buttons
            self.splash_screen_btn.update(self.game_display)
            self.draw_vision_button.update(self.game_display)
            #redraw window
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
