import tkinter
from tkinter import *


class GUI:

    def __init__(self):
        self.screen = tkinter.Canvas(width=400, height=600, highlightthickness=0)
        self.screen.master.overrideredirect(True)
        # moving screen to right side of screen

        self.screen.master.geometry("+950+0")
        self.screen.master.lift()
        self.screen.master.wm_attributes("-topmost", True)
        self.screen.master.wm_attributes("-disabled", True)
        # screen.master.wm_attributes("-alpha", 0.8) # don't need this, it makes the screen whitish and the letters
        # hard to read
        self.screen.master.wm_attributes('-transparentcolor', 'white')  # Makes the screen clear
        self.text = Text(self.screen, width=25, height=40)  # The best way to adjust the canvas screen space
        font_tuple = ("Times new roman", 20, "bold")  # Can adjust the font configuration
        self.text.configure(font=font_tuple)

    def start_screen(self):
        self.screen.pack()
        self.screen.master.bind('<Control-c>', quit)
        self.screen.master.bind('<Control-h>', self.show_screen)  # doesn't work yet
        self.screen.master.bind('<Control-s>', self.hide_screen)
        self.screen.mainloop()

    def insert_text(self, text_to_enter):
        self.text.insert('1.0', text_to_enter)
        self.text.pack()

    def quit(self, event):  # quits the program
        print("you pressed control c")
        self.screen.master.quit()  # quits the program

    def hide_screen(self, event):  # hides the program
        print("you pressed control s")
        self.screen.master.withdraw()  # hides the window

    def show_screen(self, event):  # shows the program (DOESN'T work yet)
        print("you pressed control g")
        self.screen.master.deiconify()  # shows the window


def main():
    app = GUI()

    app.start_screen()


if __name__ == '__main__':
    main()
