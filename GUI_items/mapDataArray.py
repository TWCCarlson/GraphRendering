# This is the array holding all the map information:
# tile counts and ids
# image paths
# etc
# Will have export/input methods
import tkinter as tk
# Import regex matching for use in map export
import re
# Import json structuring
import json

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
        # Pull the imagepath for each tile
        nodeList = []
        for colIndex in range(len(self.mapArray)):
            for rowIndex in range(len(self.mapArray[0])):
                # The map array contains the filepath for each tile's image
                filePath = self.mapArray[colIndex][rowIndex]
                if filePath != ' ':
                    # Regexically grab the image name
                    fileID = re.search(r"(?<=\\tileSelectorDefaultImages\\)(.*?)(?=.png)", filePath).group()
                    # From that, regexically grab the tile type
                    tileType = re.search(r"(edge)|(charge)|(deposit)|(pickup)|(rest)|(void)", fileID).group()
                    # Regexically find the edges that exist on the tile
                    tileEdgeDirections = re.findall(r"(N|W|S|E)", fileID)
                    # Translate the list to a dictionary
                    tileEdgeDict = {
                        "N": tileEdgeDirections.count("N"),
                        "W": tileEdgeDirections.count("W"),
                        "S": tileEdgeDirections.count("S"),
                        "E": tileEdgeDirections.count("E")
                    }
                    print(tileEdgeDirections)
                    # Save all the information about the node into a structure
                    nodeData = {
                        "nodePosition": {
                            "X": rowIndex,
                            "Y": colIndex
                        },
                        "nodeStyle": filePath,
                        "nodeType": tileType,
                        "nodeEdges": tileEdgeDict
                    }
                    nodeList.append(nodeData)
        mapData = json.dumps(nodeList, indent=4)
        print(mapData)