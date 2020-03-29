from game import game
from game_settings import *
from course_creator import course_creator
from tkinter import *

window_width = 350
window_height = 300

#get some screen information
x = game_window_width/2 - window_width/2
y = game_window_height/2 - window_height/2

window = Tk()

def go_to_game():
    window.destroy()
    my_game = game()
    my_game.run()

def go_to_course_creator():
    window.destroy()
    create_course = course_creator()
    create_course.run()

#displaying the splash screen
def show_splash_screen():
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.title("Racer")

    lbl = Label(window, text="Racer", font=("", 50))
    lbl.place(relx=.5, rely=.3, anchor="c")

    btn = Button(window, text="Go to Course Creator", bg="gray", fg="white", command=go_to_course_creator)
    btn.config(height = 1, width = 20)
    btn.place(relx=.5, rely=.7, anchor="c")

    btn2 = Button(window, text="Play Game!", bg="green", fg="white", command=go_to_game)
    btn2.config(height = 1, width = 10)
    btn2.place(relx=.5, rely=.6, anchor="c")
    window.mainloop()

if __name__ == '__main__':
    show_splash_screen()
