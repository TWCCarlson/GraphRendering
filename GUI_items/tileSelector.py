# Module which allows the selection of tile type before floor painting
import tkinter as tk
# Import special styles
from tkinter import FLAT, RIDGE
# Import ability to search OS directories
import os

import PIL.ImageTk
import PIL.Image

# Sizing values, static throughout code
frameHeight = 150
frameWidth = 180
frameBorderWidth = 5
frameRelief = RIDGE
baselinePad = 10
scrollbarWidth = 20
canvasWidth = 145
canvasHeight = frameHeight - 2*baselinePad
canvasMaxLen = 1000
buttonRelief = FLAT
buttonSize = 32


# The section in the main window which contains everything in the module
class tileSelector(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=frameHeight, width=frameWidth, borderwidth=frameBorderWidth, relief=frameRelief)
        self.parent = parent # The host window is the parent of this widget
        
        # Make a canvas that holds the different options
        self.selectorCanvas = selectorCanvas(self)

        # Use a scrollbar in case there are many icons to choose from
        self.ybar = tk.Scrollbar(self)
        self.ybar["width"] = scrollbarWidth
        self.ybar["orient"] = "vertical"
        self.ybar["command"] = self.selectorCanvas.yview
        self.ybar.grid(column=1, row=0, sticky="NS") # It should exist as the 2nd item in the row, stuck to the top and bottom of the parent frame

        # Make the widget size static regardless of what it contains
        self.grid_propagate(False)

        # Usage properties
        self.tileOptions = [] # Holds all the currently loaded options

        # Add the widget to the window
        self.grid(row=0, column=0, padx=baselinePad, pady=baselinePad, sticky="N") # Sticky makes the cell stay north
        
class selectorCanvas(tk.Canvas):
    # Create the space containing the tiles
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self["width"] = canvasWidth     # Control the display section width
        self["height"] = canvasHeight    # Control the display section height
        self["scrollregion"] = (0,0,0,canvasMaxLen)
        # self["yscrollcommand"] = self.parent.ybar.set
        self.grid(column=0, row=0)

        # Create a container for loaded tiles
        self.tileOpts = []
        self.tileSize = buttonSize

        # Store the location of the next button to be added
        self.nextButtonPosition = (0, 0)

        # Load the default icon set
        self.LoadDefaultTileset()

    # Function for loading the default tiles (open, station, etc)
    def LoadDefaultTileset(self):
        # Grab all the default tile icons from the package directory
        imagePaths = []
        # Retrieve current system directory filepath
        curdir = os.path.dirname(__file__)
        print(curdir)
        # Add the target directory filepath
        tardir = os.path.join(curdir, 'tileSelectorDefaultImages')
        print(tardir)
        # Iterate over all items found in the directory
        for path in os.listdir(tardir):
            # Verify file-ness
            imagePath = os.path.join(tardir, path)
            if os.path.isfile(imagePath):
                # Add the filepath to the list
                imagePaths.append(imagePath)
        # Generate buttons for each item
        self.MakeTileOpt(imagePaths)
    
    def MakeTileOpt(self, imagePaths):
        for item in imagePaths:
            self.tileOpts.append(TileButton(self, item, self.nextButtonPosition))
            # Update the next button's position
            self.nextButtonPosition = (self.nextButtonPosition[0] + self.tileSize + 2,
            self.nextButtonPosition[1])
            # If the next button would run off the linewidth, move down a row
            if self.nextButtonPosition[0] > canvasWidth - buttonSize:
                self.nextButtonPosition = (0, self.nextButtonPosition[1] + buttonSize + 2)

class TileButton(tk.Button):
    def __init__(self, parent, imagePath, buttonPosition):
        tk.Button.__init__(self, parent, relief=FLAT)
        self.parent = parent
        # Store the args for future references to the class instance
        self.path = imagePath
        self.buttonPosition =  buttonPosition
        # Draw the window acting as the button display
        self.parent.create_window(self.buttonPosition[0], self.buttonPosition[1],
            window = self, anchor = tk.NW)
        self.tile = Tile(self.path, self.parent.tileSize)
        self["image"] = self.tile.image
        self["command"] = lambda i = len(parent.tileOpts): parent.selectTile(i)

        
class Tile(): #class structure to hold images
    def __init__(self, path, size):
        self.size = size
        self.path = path
        self.image  = PIL.Image.open(open(path, 'rb')) #open a regular PIL image
        self.image = self.image.resize((self.size, self.size)) #resize the image to size we want tiles
        self.image = PIL.ImageTk.PhotoImage(self.image) #convert image to a tk displayable image