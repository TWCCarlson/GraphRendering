# This is the array holding all the map information:
# tile counts and ids
# image paths
# etc
# Will have export/input methods
import tkinter as tk

class mapDataArray:
    def __init__(self, parent, dims):
        self.parent = parent
        # Map dimensions
        self.mapWidth = dims[0]
        self.mapHeight = dims[1]

        # Create an integer array 
        self.mapArray = []
        for i in range(self.mapHeight):
            row = []
            for j in range(self.mapWidth):
                row.append(" ") # Empty items are empty - distinct from zeros
            self.mapArray.append(row)
        
        # Create a matching array with imagepaths for displaying in app
        self.canvasArray = []
        for i in range(self.mapHeight):
            row = []
            for j in range(self.mapWidth):
                row.append(" ") # Empty items are empty - distinct from zeros
            self.canvasArray.append(row)

    def Save(self, path, saveType):
        print(self.mapArray)
        print(self.canvasArray)

        # Create a dictionary of all the images used
        # ^ Static, in this use case
        # Translate the path array into graphmap = (node existence, (edge directions), node type)
        # Save as JSON (imagepaths, graphmap)