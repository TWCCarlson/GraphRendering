# The frame and objects which contain the design space for making a map
import tkinter as tk
# Import special styles
from tkinter import FLAT, RIDGE

toolboxWidth = 180
screenUsage = 0.75
borderWidth = 5
canvasPad = 32
canvasSizeTemp = 4000
tileSize = 32

class designSpace(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        # Configure appearance
        # Save these for reference downstream
        self.width = (self.parent.winfo_screenwidth() - toolboxWidth) * screenUsage
        self.height = (self.parent.winfo_screenheight()) * screenUsage
        self["width"] = self.width
        self["height"] = self.height
        self["relief"] = RIDGE
        self["borderwidth"] = borderWidth

        # Implement scrolling
        self.ybar = tk.Scrollbar(self, orient="vertical")
        self.xbar = tk.Scrollbar(self, orient="horizontal")

        # Build the canvas inside the frame
        self.canvas = designCanvas(self)
        self.ybar["command"] = self.canvas.yview
        self.xbar["command"] = self.canvas.xview
        self.ybar.grid(column=1, row=0, sticky="ns")
        self.xbar.grid(column=0, row=1, sticky="ew")

        # Render component
        self.grid_propagate(False)
        self.grid(row=0, column=1, pady=borderWidth, padx=borderWidth, rowspan=2)

class designCanvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.parent = parent

        # Configure canvas appearance
        self["width"] = self.parent.width - canvasPad
        self["height"] = self.parent.height - canvasPad
        self["bg"] = "#abbcd6"
        self["yscrollcommand"] = self.parent.ybar.set
        self["xscrollcommand"] = self.parent.xbar.set
        self["scrollregion"] = (0,0,canvasSizeTemp,canvasSizeTemp) # TODO: #1 make this adjust to grid size
        self.xview_moveto("0.0")
        self.yview_moveto("0.0")

        # Create visible divisions on the canvas to delineate tiles
        for i in range(int(canvasSizeTemp/tileSize)+1):
            self.create_line(i* tileSize, 0, i * tileSize, canvasSizeTemp, fill="light gray")
        for i in range(int(canvasSizeTemp/tileSize)+1):
            self.create_line(0, i* tileSize, canvasSizeTemp, i * tileSize, fill="light gray")

        # Enable hotkey scrolling
        # TODO: enable hotkey scrolling

        # Binding inputs
        self.bind("<Button-1>", self.selectTile)    # Single click
        self.bind("<B1-Motion>", self.selectTile)   # Click-drag

        # Render component
        self.grid(column=0, row=0)

    def selectTile(self, event):
        xScrollDist = self.parent.xbar.get()[0]
        yScrollDist = self.parent.ybar.get()[0]
        # Convert the click location to a tile location using scrollbar position data
        # Scrollbar fraction * total canvas size + click event view location / tileSize, floored gives tile ID for column/row
        self.selectedTileX = int((xScrollDist * canvasSizeTemp + event.x)/tileSize)
        self.selectedTileY = int((yScrollDist * canvasSizeTemp + event.y)/tileSize)
        self.selectedTile = (self.selectedTileX, self.selectedTileY)

        # Execute click effect
        self.setTile()

    def setTile(self):
        if self.parent.parent.toolSelect.selectorCanvas.tool == "paint":
            print("paint tile")

        if self.parent.parent.toolSelect.selectorCanvas.tool == "erase":
            print("erase tile")

        if self.parent.parent.toolSelect.selectorCanvas.tool == "fill":
            print("fill region")

        if self.parent.parent.toolSelect.selectorCanvas.tool == "fillErase":
            print("void region")
    
