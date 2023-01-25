from game import game
from game_settings import *
from course_creator import course_creator
from tkinter import *
import time

window_width = 350
window_height = 300

#get some screen information
x = game_window_width/2 - window_width/2
y = game_window_height/2 - window_height/2

def show_splash_screen():
    window = Tk()
    def go_to_game():
        window.destroy()
        my_game = game()
        my_game.run()
    def go_to_course_creator():
        window.destroy()
        create_course = course_creator()
        create_course.run()
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.title("RacerAI")
    lbl = Label(window, text="RacerAI", font=("", 50))
    lbl.place(relx=.5, rely=.3, anchor="c")
    btn = Button(window, text="Course Creator", bg="gray", fg="white", command=go_to_course_creator)
    btn.config(height = 1, width = 20)
    btn.place(relx=.5, rely=.85, anchor="c")
    btn2 = Button(window, text="Train AI", bg="green", fg="white", command=go_to_game)
    btn2.config(height = 1, width = 10)
    btn2.place(relx=.5, rely=.7, anchor="c")
    window.protocol("WM_DELETE_WINDOW", sys.exit)
    window.mainloop()

if __name__ == '__main__':
    show_splash_screen()
