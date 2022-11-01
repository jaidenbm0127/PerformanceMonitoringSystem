import tkinter
from tkinter import *


class DataShow:
    screen = tkinter.Canvas(width=400, height=800, highlightthickness=0)
    screen.master.overrideredirect(True)
    screen.master.geometry("+950+0")  # moving screen to right side of screen
    screen.master.lift()
    screen.master.wm_attributes("-topmost", True)
    screen.master.wm_attributes("-disabled", True)
    screen.master.wm_attributes('-transparentcolor', 'white')  # Makes the screen clear

    text = Text(screen, width=25, height=40)  # The best way to adjust the canvas screen space
    text.pack()
    text.insert('1.0', 'This is a test ')
    Font_tuple = ("Times new roman", 13, "bold")  # Can adjust the font configuration
    text.configure(font=Font_tuple)

    def show_data(data, text=text):
        text.insert('1.0', data)
        text.pack()
        return data

    show_data('Process 1\n')
    show_data('Process 2\n')
    show_data('Process 3\n')

    def quit(event, screen=screen):  # quits the program
        print("you pressed control c")
        screen.master.quit()  # quits the program

    def hide_screen(event, screen=screen):  # hides the program
        print("you pressed control s")
        screen.master.withdraw()  # hides the window

    def show_screen(event, screen=screen):  # shows the program (DOESN'T work yet)
        print("you pressed control g")
        screen.master.deiconify()  # shows the window

    screen.pack()
    screen.master.bind('<Control-c>', quit)
    screen.master.bind('<Control-h>', show_screen)  # doesn't work yet
    screen.master.bind('<Control-s>', hide_screen)
    screen.mainloop()
