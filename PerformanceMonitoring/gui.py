import tkinter
from tkinter import Text

screen = tkinter.Canvas(width=400, height=800, highlightthickness=0)
screen.master.overrideredirect(True)
screen.master.geometry("+0+0")
screen.master.lift()
screen.master.wm_attributes("-topmost", True)
screen.master.wm_attributes("-disabled", True)
screen.create_rectangle(0, 0, 400, 800, fill='black')
screen.master.wm_attributes("-alpha", 0.4)

screen.create_text(200,150,fill="white",font="Times 15  bold",
text="Click the bubbles that are multiples of two.") #option 1 -- less text with black background
#
# text = Text(screen, width=25, height=40)  # The best way to adjust the canvas screen space
# text.pack()
# text.insert('1.0', 'This is a test ')
#
# Font_tuple = ("Times new roman", 15, "bold")  # Can adjust the font configuration
# text.configure(font=Font_tuple)

screen.pack()
screen.mainloop()