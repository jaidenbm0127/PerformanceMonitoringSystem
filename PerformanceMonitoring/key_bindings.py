from tkinter import NORMAL, Text, LEFT

from prompt_toolkit.key_binding import KeyBindings

from PerformanceMonitoring.gui import screen

bindings = KeyBindings()


@bindings.add('a')
def _(event):
    " Do something if 'a' has been pressed. "
    ...


@bindings.add('escape')
def _hide(event):
    text = Text(screen, width=25, height=40, state=NORMAL)  # The best way to adjust the canvas screen space
    # (state='disabled') <-- can be used in line above to keep people from typing in window accidently
    text.pack(side=LEFT)
    # text.forget.pack() to hide data
    text.insert('1.0', 'This is a test ')

    font_tuple = ("Times new roman", 20, "bold")  # Can adjust the font configuration
    text.configure(font=font_tuple)
