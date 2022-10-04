from tkinter import *
import tkinter as tk


root = Tk()

root.geometry("700x350")

root.config(bg='#add123')

root.wm_attributes('-transparentcolor', '#add123')
root.wm_attributes('-fullscreen', 'True')

label = tk.Label(root, text="Hello, This is a TEST")
label.pack()
root.mainloop()



