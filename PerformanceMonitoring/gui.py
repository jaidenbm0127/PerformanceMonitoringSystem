import tkinter
import ctypes
from tkinter import *

ctypes.windll.shcore.SetProcessDpiAwareness(1) #makes the font sharper

class showData:
    screen = tkinter.Canvas(width=145, height=650, highlightthickness=0)
    screen.master.overrideredirect(True)
    screen.master.lift()
    screen.master.wm_attributes("-topmost", True)
    screen.master.wm_attributes("-disabled", True)
    screen.master.wm_attributes('-transparentcolor', 'white')  # Makes the screen clear


    text = Text(screen, width=145, height=40)  # The best way to adjust the canvas screen space
    text.tag_configure("tag_name", justify='right')
    text.pack()
    text.insert('1.0', 'This is a test on how to make tkinter text to appear on the right side only if it not on the right thannn but than coool things happen and its so much fun right? noooooooooo things are not allways fun duhhh because it things and things. get ittttttt hahahahha ')
    Font_tuple = ("Times new roman", 13, "bold")  # Can adjust the font configuration
    text.configure(font=Font_tuple)

    def show_data(data, text=text):
        text.insert('1.0', data)
        text.pack()
        return data

    show_data('Process 1\n')
    show_data('Process 2\n')
    show_data('Process 3\n')

    text.tag_add("tag_name", "1.0", "end")

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
