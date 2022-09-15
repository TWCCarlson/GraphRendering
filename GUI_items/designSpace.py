# The frame and objects which contain the design space for making a map
import tkinter as tk
# Import special styles
from tkinter import FLAT, RIDGE

toolboxWidth = 180
screenUsage = 0.75
borderWidth = 5
canvasPad = 32
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

        # Scrolling
        self.bind('<Enter>', self.bindToMousewheel)
        self.bind('<Leave>', self.unbindMousewheel)

    def bindToMousewheel(self, event):
        self.bind_all("<MouseWheel>", self.mousewheelAction)
        self.bind_all("<Shift-MouseWheel>", self.shiftMousewheelAction)

    def unbindMousewheel(self, event):
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Shift-MouseWheel>")

    def mousewheelAction(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def shiftMousewheelAction(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

class designCanvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self.canvasWidth = self.parent.parent.mapData.mapWidth * tileSize
        self.canvasHeight = self.parent.parent.mapData.mapHeight * tileSize

        # Configure canvas appearance
        self.redrawGridlines()

        # Create visible divisions on the canvas to delineate tiles
        self.drawGridlines()

        # Enable hotkey scrolling
        # TODO: enable hotkey scrolling

        # Binding inputs
        self.bind("<Button-1>", self.selectTile)    # Single click
        self.bind("<B1-Motion>", self.selectTile)   # Click-drag
        self.bind("<ButtonRelease-1>", self.setBoxSelect)

        # Render component
        self.grid(column=0, row=0, sticky=tk.NW)

    def redrawGridlines(self):
        # Update the canvas width in case of redraws from new/load
        self.canvasWidth = self.parent.parent.mapData.mapWidth * tileSize
        self.canvasHeight = self.parent.parent.mapData.mapHeight * tileSize

        self["width"] = min(self.parent.width - canvasPad, self.canvasWidth)
        self["height"] = min(self.parent.height - canvasPad, self.canvasWidth)
        self["bg"] = "#abbcd6"
        self["yscrollcommand"] = self.parent.ybar.set
        self["xscrollcommand"] = self.parent.xbar.set
        self["scrollregion"] = (0,0,self.canvasWidth,self.canvasHeight)
        self.xview_moveto("0.0")
        self.yview_moveto("0.0")

    def drawGridlines(self):
        # Update the canvas width in case of redraws from new/load
        print(self.parent.parent.mapData.mapWidth)
        self.canvasWidth = self.parent.parent.mapData.mapWidth * tileSize
        self.canvasHeight = self.parent.parent.mapData.mapHeight * tileSize

        # Draw lines
        for i in range(int(self.canvasWidth/tileSize)+1):
            self.create_line(i* tileSize, 0, i * tileSize, self.canvasWidth, fill="light gray")
        for i in range(int(self.canvasHeight/tileSize)+1):
            self.create_line(0, i* tileSize, self.canvasHeight, i * tileSize, fill="light gray")

    def selectTile(self, event):
        # Reference to current tool
        self.currentTool = self.parent.parent.toolSelect.selectorCanvas.tool

        xScrollDist = self.parent.xbar.get()[0]
        yScrollDist = self.parent.ybar.get()[0]
        # Convert the click location to a tile location using scrollbar position data
        # Scrollbar fraction * total canvas size + click event view location / tileSize, floored gives tile ID for column/row
        self.selectedTileX = int((xScrollDist * self.canvasWidth + event.x)/tileSize)
        self.selectedTileY = int((yScrollDist * self.canvasHeight + event.y)/tileSize)
        self.selectedTile = (self.selectedTileX, self.selectedTileY)

        # Execute click effect
        self.setTile()

    def setTile(self):
        # Reference variable to the map data
        mapData = self.parent.parent.mapData
        # Reference to current tool
        self.currentTool = self.parent.parent.toolSelect.selectorCanvas.tool

        if self.currentTool == "paint":
            # Capture information about what's being painted
            currentImage = self.parent.parent.tileSelect.currentImage
            currentImagePath = self.parent.parent.tileSelect.currentImagePath
            currentImageIndex = self.parent.parent.tileSelect.currentImageIndex

            # Remove whatever is there already if there is something
            if mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]] != " ":
                self.delete(mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]])
                mapData.mapArray[self.selectedTile[0]][self.selectedTile[1]] = ' '
                mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]] = ' '
            
            # Draw the new tile in its place
            paintImage = self.create_image(self.selectedTile[0]*tileSize, self.selectedTile[1]*tileSize, image=currentImage, anchor=tk.NW)
            mapData.mapArray[self.selectedTile[0]][self.selectedTile[1]] = currentImagePath
            mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]] = currentImageIndex

        if self.currentTool == "erase":
            # Remove whatever is on the tile
            self.delete(mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]])
            # and from the data arrays
            mapData.mapArray[self.selectedTile[0]][self.selectedTile[1]] = ' '
            mapData.canvasArray[self.selectedTile[0]][self.selectedTile[1]] = ' '

        if self.currentTool == "fill" or self.currentTool == "fillErase":
            # This only draws a highlight of the region selected
            if self.parent.parent.toolSelect.boxStartPos == []:
                # Save the initial position of the box
                self.parent.parent.toolSelect.boxStartPos = [self.selectedTile[0],self.selectedTile[1]]
            else:
                try:
                    # Remove a previously drawn box if it exists
                    self.delete(self.rectangleDraw)
                except:
                    pass
                # and draw a new one
                self.rectangleDraw = self.create_rectangle(
                    self.parent.parent.toolSelect.boxStartPos[0]*tileSize,
                    self.parent.parent.toolSelect.boxStartPos[1]*tileSize,
                    self.selectedTileX*tileSize,
                    self.selectedTileY*tileSize,
                    dash=(5,5),
                    outline="black"
                )
                # Handling the operation has to be bound to a mouse release in this config

    def setBoxSelect(self, event):
        if self.currentTool == "fill" or self.currentTool == "fillErase":
            # Handle the two different kinds of area selections
            # Capture the box corner data
            self.boxStartPos = self.parent.parent.toolSelect.boxStartPos*tileSize

            # Clear the drawn rectable
            self.delete(self.rectangleDraw)

            # Target cells between the corners
            # <Motion> will have the end corner highlighted for us as selectedTile
            for incrementX in range(abs(self.boxStartPos[0] - self.selectedTileX)):
                # print("COLUMN: " + str(incrementX))
                for incrementY in range(abs(self.boxStartPos[1] - self.selectedTileY)):
                    # print("ROW: " + str(incrementY))
                    # If the first corner is on the left
                    if self.boxStartPos[0] < self.selectedTileX:
                        # And the end corner is lower
                        if self.boxStartPos[1] < self.selectedTileY:
                            # Fill left(startX)->right(endX) top(startY)->bottom(endY)
                            self.fillTile(incrementX, incrementY, self.boxStartPos[0], self.boxStartPos[1])
                        # And the end corner is higher
                        if self.boxStartPos[1] > self.selectedTileY:
                            # Fill left(startX)->right(endX) top(endY)->bottom(startY)
                            self.fillTile(incrementX, incrementY, self.boxStartPos[0], self.selectedTileY)
                    # If the first corner is on the right
                    if self.boxStartPos[0] > self.selectedTileX:
                        # And the end corner is lower
                        if self.boxStartPos[1] < self.selectedTileY:
                            # Fill left(endX)->right(startX) top(startY)->bottom(endY) 
                            self.fillTile(incrementX, incrementY, self.selectedTileX, self.boxStartPos[1])
                        # And the end corner is higher
                        if self.boxStartPos[1] > self.selectedTileY:
                            # Fill left(endX)->right(startX) top(endY)->bottom(startY)
                            self.fillTile(incrementX, incrementY, self.selectedTileX, self.selectedTileY)

                # After filling, delete the rectangle and free up the start square
                self.delete(self.rectangleDraw)
                self.parent.parent.toolSelect.boxStartPos = []

    def fillTile(self, incrementX, incrementY, startX, startY):
        # Ingests: the current iterative tile from the corner to begin at
        # Paints the tile accordingly
        # print("PAINTING TILE FROM CORNER: (" + str(startX) + "," + str(startY) + ")")
        # print("PAINTING TILE: (" + str(incrementX + startX) + "," + str(incrementY + startY) + ")")
        # Reference variable to the map data
        mapData = self.parent.parent.mapData
        currentImage = self.parent.parent.tileSelect.currentImage
        currentImagePath = self.parent.parent.tileSelect.currentImagePath

        # Clear out the tile if it already contains something
        if mapData.canvasArray[incrementX + startX][incrementY + startY] != " ":
            self.delete(mapData.canvasArray[incrementX + startX][incrementY + startY])
        mapData.canvasArray[incrementX + startX][incrementY + startY] = ' '
        mapData.mapArray[incrementX + startX][incrementY + startY] = ' '

        # Draw the new tile if filling
        if self.currentTool == "fill":
            paintImage = self.create_image((incrementX + startX)*tileSize, (incrementY + startY)*tileSize, image=currentImage, anchor=tk.NW)
            mapData.mapArray[incrementX + startX][incrementY + startY] = currentImagePath
            mapData.canvasArray[incrementX + startX][incrementY + startY] = paintImage


