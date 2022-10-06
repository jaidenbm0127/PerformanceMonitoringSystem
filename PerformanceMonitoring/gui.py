import tkinter
from tkinter import Text

screen = tkinter.Canvas(width=300, height=300, highlightthickness=0)
screen.master.overrideredirect(True)
screen.master.geometry("+0+0")
screen.master.lift()
screen.master.wm_attributes("-topmost", True)
screen.master.wm_attributes("-disabled", True)
screen.create_rectangle(0, 0, 300, 300, fill="black")
screen.master.wm_attributes("-alpha", 0.5)

text = Text(screen, height= 2)
text.pack()
text.insert('1.0', 'This is a test ')




screen.pack()
screen.mainloop()

