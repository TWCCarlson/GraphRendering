# Visual designer for creating floormaps
# PURPOSE:
# Accepts user inputs (clicks)
# constructs a graph
# exports an adjacency list
# METHOD:
# GUI created with Tkinter

# Import tkinter itself
import tkinter as tk

# Import the classdefs from the modules directory
from GUI_items import *

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # Initialize main window
        self.title("FloorDesign - GUI")
        self.tileSelect = tileSelector(self)
        self.toolSelect = toolSelector(self)
        self.mainloop() # Blocking call to render the app

app = App()