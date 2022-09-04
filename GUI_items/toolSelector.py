# Module which allows user to select whether they are painting, erasing, or filling an area with tiles
import tkinter as tk
# Import special styles
from tkinter import FLAT, RIDGE
# Import tile object class
from .tile import Tile
# Import filesystem navigation
import os

# Sizing values, static
frameHeight = 47
frameWidth = 179
frameBorderWidth = 5
frameRelief = RIDGE
baselinePad = 10
canvasWidth = 166
canvasHeight = frameHeight - 1.5*baselinePad
buttonSize = 32
buttonWidth = buttonSize + 4

# The frame contains everything in this module
class toolSelector(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=frameHeight, width=frameWidth, borderwidth=frameBorderWidth, relief=frameRelief)
        self.parent = parent

        # Make the widget size static regardless of what it contains
        self.grid_propagate(False)

        # Make a canvas to hold the tool selections
        self.selectorCanvas = selectorCanvas(self)

        # Usage properties
        self.toolOptions = [] # Holds all the tool choices

        # Place the frame in the window
        self.grid(row=1, column=0, padx=baselinePad, pady=baselinePad)

class selectorCanvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent, bg="skyblue")
        self.parent = parent

        # Canvas props
        self["width"] = canvasWidth
        self["height"] = canvasHeight
        self.grid(column=0, row=0, sticky = "n")
        self.tileSize = buttonSize

        # Image paths
        self.paintTool_img = Tile('GUI_items/toolSelectorDefaultImages/Pointer.png', buttonSize).image
        self.eraseTool_img = Tile('GUI_items/toolSelectorDefaultImages/Eraser.png', buttonSize).image
        self.fillTool_img = Tile('GUI_items/toolSelectorDefaultImages/boxSelect.png', buttonSize).image
        self.fillErase_img = Tile('GUI_items/toolSelectorDefaultImages/boxErase.png', buttonSize).image

        # Paint tool
        self.paintTool = tk.Button(self, command=self.paint, image=self.paintTool_img, width=buttonWidth)
        self.paintTool.grid(column=0, row=0)

        # Erase tool
        self.eraseTool = tk.Button(self, command=self.erase, image=self.eraseTool_img, width=buttonWidth)
        self.eraseTool.grid(column=1, row=0)

        # Fill tool
        self.fillTool = tk.Button(self, command=self.fill, image=self.fillTool_img, width=buttonWidth)
        self.fillTool.grid(column=2, row=0)

        # Fill erase tool
        self.fillErase = tk.Button(self, command=self.fillErase, image=self.fillErase_img, width=buttonWidth)
        self.fillErase.grid(column=3, row=0)

        self.paint()


    def paint(self):
        self.tool = "paint"
        # Set the painter image to show activity
        self.paint_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/PointerActive.png')
        self.paintTool.config(image=self.paint_img)
        # Deactivate the other images
        self.erase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Eraser.png')
        self.eraseTool.config(image=self.erase_img)
        self.fill_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxSelect.png')
        self.fillTool.config(image=self.fill_img)
        self.fillErase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxErase.png')
        self.fillErase.config(image=self.fillErase_img)

    def erase(self):
        self.tool = "erase"
        # Set the eraser image to show activity
        self.erase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/EraserActive.png')
        self.eraseTool.config(image=self.erase_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Pointer.png')
        self.paintTool.config(image=self.paint_img)
        self.fill_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxSelect.png')
        self.fillTool.config(image=self.fill_img)
        self.fillErase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxErase.png')
        self.fillErase.config(image=self.fillErase_img)

    def fill(self):
        self.tool = "fill"
        # Set the eraser image to show activity
        self.fill_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxSelectActive.png')
        self.fillTool.config(image=self.fill_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Pointer.png')
        self.paintTool.config(image=self.paint_img)
        self.erase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Eraser.png')
        self.eraseTool.config(image=self.erase_img)
        self.fillErase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxErase.png')
        self.fillErase.config(image=self.fillErase_img)
        
    def fillErase(self):
        self.tool = "fillErase"
        # Set the image to show activity
        self.fillErase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxEraseActive.png')
        self.fillErase.config(image=self.fillErase_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Pointer.png')
        self.paintTool.config(image=self.paint_img)
        self.erase_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/Eraser.png')
        self.eraseTool.config(image=self.erase_img)
        self.fill_img = tk.PhotoImage(file='GUI_items/toolSelectorDefaultImages/boxSelect.png')
        self.fillTool.config(image=self.fill_img)