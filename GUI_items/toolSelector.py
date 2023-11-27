# Module which allows user to select whether they are painting, erasing, or filling an area with tiles
import tkinter as tk
# Import special styles
from tkinter import FLAT, RIDGE
# Import tile object class
from .tile import Tile
# Import filesystem navigation
import os

# TODO: #2 hover tooltips/labels

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
        self.boxStartPos = []

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
        curdir = os.path.dirname(__file__)
        self.pointerDir = os.path.join(curdir, 'toolSelectorDefaultImages/Pointer.png')
        self.pointerActiveDir = os.path.join(curdir, 'toolSelectorDefaultImages/PointerActive.png')
        self.eraserDir = os.path.join(curdir, 'toolSelectorDefaultImages/Eraser.png')
        self.eraserActiveDir = os.path.join(curdir, 'toolSelectorDefaultImages/EraserActive.png')
        self.boxSelectDir = os.path.join(curdir, 'toolSelectorDefaultImages/boxSelect.png')
        self.boxSelectActiveDir = os.path.join(curdir, 'toolSelectorDefaultImages/boxSelectActive.png')
        self.boxEraseDir = os.path.join(curdir, 'toolSelectorDefaultImages/boxErase.png')
        self.boxEraseActiveDir = os.path.join(curdir, 'toolSelectorDefaultImages/boxEraseActive.png')

        self.paintTool_img = Tile(self.pointerDir, buttonSize).image
        self.eraseTool_img = Tile(self.eraserDir, buttonSize).image
        self.fillTool_img = Tile(self.boxSelectDir, buttonSize).image
        self.fillErase_img = Tile(self.boxEraseDir, buttonSize).image

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
        self.paint_img = tk.PhotoImage(file=self.pointerActiveDir)
        self.paintTool.config(image=self.paint_img)
        # Deactivate the other images
        self.erase_img = tk.PhotoImage(file=self.eraserDir)
        self.eraseTool.config(image=self.erase_img)
        self.fill_img = tk.PhotoImage(file=self.boxSelectDir)
        self.fillTool.config(image=self.fill_img)
        self.fillErase_img = tk.PhotoImage(file=self.boxEraseDir)
        self.fillErase.config(image=self.fillErase_img)

    def erase(self):
        self.tool = "erase"
        # Set the eraser image to show activity
        self.erase_img = tk.PhotoImage(file=self.eraserActiveDir)
        self.eraseTool.config(image=self.erase_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file=self.pointerDir)
        self.paintTool.config(image=self.paint_img)
        self.fill_img = tk.PhotoImage(file=self.boxSelectDir)
        self.fillTool.config(image=self.fill_img)
        self.fillErase_img = tk.PhotoImage(file=self.boxEraseDir)
        self.fillErase.config(image=self.fillErase_img)

    def fill(self):
        self.tool = "fill"
        # Set the eraser image to show activity
        self.fill_img = tk.PhotoImage(file=self.boxSelectActiveDir)
        self.fillTool.config(image=self.fill_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file=self.pointerDir)
        self.paintTool.config(image=self.paint_img)
        self.erase_img = tk.PhotoImage(file=self.eraserDir)
        self.eraseTool.config(image=self.erase_img)
        self.fillErase_img = tk.PhotoImage(file=self.boxEraseDir)
        self.fillErase.config(image=self.fillErase_img)
        
    def fillErase(self):
        self.tool = "fillErase"
        # Set the image to show activity
        self.fillErase_img = tk.PhotoImage(file=self.boxEraseActiveDir)
        self.fillErase.config(image=self.fillErase_img)
        # Deactivate the other images
        self.paint_img = tk.PhotoImage(file=self.pointerDir)
        self.paintTool.config(image=self.paint_img)
        self.erase_img = tk.PhotoImage(file=self.eraserDir)
        self.eraseTool.config(image=self.erase_img)
        self.fill_img = tk.PhotoImage(file=self.boxSelectDir)
        self.fillTool.config(image=self.fill_img)