import tkinter
import ctypes
from tkinter import *
import pandas as pd

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # makes the font sharper

class showData:

    screen = tkinter.Canvas(width=400, height=600, highlightthickness=0)
    screen.master.overrideredirect(True)
    screen.master.geometry("+950+0") #move screen
    screen.master.lift()
    screen.master.wm_attributes("-disabled", True)
    screen.create_rectangle(0, 0, 400, 600, fill='black')
    screen.master.wm_attributes("-alpha", 0.7)

    text = Text(screen, width=100, height=33)  # The best way to adjust the canvas screen space
    text.pack()
    Font_tuple = ("Times new roman", 13, "bold")  # Can adjust the font configuration
    text.configure(font=Font_tuple, fg= "black")

    def show_data(data, text=text):
        text.insert('1.0', data)
        text.pack()
        return data

    dataframe1 = pd.read_excel('Data.xlsx')

    print(dataframe1)
    show_data(dataframe1)

    screen.pack()
    screen.mainloop()
