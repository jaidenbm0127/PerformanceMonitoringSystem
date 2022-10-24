import tkinter
from tkinter import *
from prompt_toolkit.key_binding import KeyBindings
from pynput import keyboard


screen = tkinter.Canvas(width=400, height=600, highlightthickness=0)
screen.master.overrideredirect(True)
#moving screen to right side of screen

screen.master.geometry("+950+0")
screen.master.lift()
screen.master.wm_attributes("-topmost", True)
screen.master.wm_attributes("-disabled", True)
#screen.master.wm_attributes("-alpha", 0.8) # don't need this, it makes the screen whitish and the letters hard to read
screen.master.wm_attributes('-transparentcolor', 'white') #Makes the screen clear


text = Text(screen, width=25, height=40)  # The best way to adjust the canvas screen space
text.insert('1.0', 'test')
font_tuple = ("Times new roman", 20, "bold")  # Can adjust the font configuration
text.configure(font=font_tuple)
text.pack()


def show_data(data):
    text.insert('1.0', data)
    text.pack()
    return data


show_data('Process 1\n')
show_data('Process 2\n')
show_data('Process 3\n')


def quit(event): #quits the program
    print("you pressed control c")
    screen.master.quit() #quits the program


def hide_screen(event): #hides the program
    print("you pressed control s")
    screen.master.withdraw() #hides the window


def show_screen(event): #shows the program (DOESN'T work yet)
    print("you pressed control g")
    screen.master.deiconify() #shows the window


screen.pack()
screen.master.bind('<Control-c>', quit)
screen.master.bind('<Control-h>', show_screen) #doesn't work yet
screen.master.bind('<Control-s>', hide_screen)
screen.mainloop()



