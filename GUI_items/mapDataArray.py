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
# Import the canvas class for ingesting a new map
from GUI_items.designSpace import designCanvas

tileSize = 32
import pprint
pp = pprint.PrettyPrinter(indent=4)

class mapDataArray:
    def __init__(self, parent, dims):
        self.parent = parent
        # Map dimensions
        self.mapWidth = dims[0]
        self.mapHeight = dims[1]

        self.generateNewMap(self.mapHeight, self.mapWidth)

    def buildReferences(self, parent):
        self.canvasReference = self.parent.canvas.canvas

    def generateNewMap(self, mapHeight, mapWidth):
        # Create an integer array 
        print(f"Generating new map: {mapWidth} x {mapHeight}")
        self.mapArray = []
        for i in range(mapHeight):
            row = []
            for j in range(mapWidth):
                row.append(" ") # Empty items are empty - distinct from zeros
            self.mapArray.append(row)
        
        # Create a matching array to hold tkinter images for tool options
        self.canvasArray = []
        for i in range(mapHeight):
            row = []
            for j in range(mapWidth):
                row.append(" ") # Empty items are empty - distinct from zeros
            self.canvasArray.append(row)

        # Create a matching array with image indexes for tool options
        self.imageIndexArray = []
        for i in range(mapHeight):
            row = []
            for j in range(mapWidth):
                row.append(" ")
            self.imageIndexArray.append(row)

        # Update the maximum dims for reference elsewhere
        self.mapHeight = mapHeight
        self.mapWidth = mapWidth

        try:
            # self.canvasReference.destroy()
            # self.parent.canvas.buildCanvas()
            self.parent.canvas.canvas.redrawGridlines()
            pass
        except:
            print("Canvas reference not yet built, proceeding with default")

    def Save(self, path, saveType):
        # print(self.mapArray)
        # print(self.canvasArray)
        # print(saveType)
        if saveType == 1:
            # print("Pruned save")
            self.SavePrune(path)
        elif saveType == 2:
            # print("Save all")
            pp.pprint(self.mapArray)
            self.SaveAll(path, self.mapArray, self.imageIndexArray)

    def SavePrune(self, path):
        # Remove empty rows and columns first
        # Pull out a column
        colsWithIndexData = []
        colsWithPathData = []
        for colIndex in range(len(self.imageIndexArray)):
            # Iterate along its cells
            sliceContainsItem = False
            for rowIndex in range(len(self.imageIndexArray[colIndex])):
                if self.imageIndexArray[colIndex][rowIndex] != " ":
                    sliceContainsItem = True
                    # pp.pprint(colIndex)
                    # pp.pprint(self.imageIndexArray[colIndex])
            if sliceContainsItem == True:
                colsWithIndexData.append(self.imageIndexArray[colIndex])
                colsWithPathData.append(self.mapArray[colIndex])

        # The result is a list of columns
        # Need to iterate through a list of rows, so transpose the list of lists
        indexTranspose = [list(i) for i in zip(*colsWithIndexData)]
        pathTranspose = [list(i) for i in zip(*colsWithPathData)]

        # From the resulting columns, pull out rows
        # print("FULL ARRAY")
        # pp.pprint(self.imageIndexArray)
        # print("FULL ARRAY TRANSPOSE")
        # imTranspose = [list(i) for i in zip(*self.imageIndexArray)]
        # pp.pprint(imTranspose)
        # print("RELEVANT COLUMNS ONLY")
        # pp.pprint(transpose)
        prunedIndexData = []
        prunedPathData = []
        for rowIndex in range(len(indexTranspose)):
            # Iterate
            sliceContainsItem = False
            for colIndex in range(len(indexTranspose[rowIndex])):
                if indexTranspose[rowIndex][colIndex] != " ":
                    sliceContainsItem = True
            if sliceContainsItem == True:
                prunedIndexData.append(indexTranspose[rowIndex])
                prunedPathData.append(pathTranspose[rowIndex])

        # pp.pprint(self.imageIndexArray)
        # print("RELEVANT ROWS ONLY")
        # pp.pprint(prunedIndexData)

        # Retranspose the array
        prunedIndexData = [list(i) for i in zip(*prunedIndexData)]
        prunedPathData = [list(i) for i in zip(*prunedPathData)]

        self.SaveAll(path, prunedPathData, prunedIndexData)

    def SaveAll(self, path, mapArray, imageIndexArray):
        # Create a dictionary of all the images used
        # ^ Static, in this use case
        # Translate the path array into graphmap = (node existence, (edge directions), node type)
        # Save as JSON (imagepaths, graphmap)
        # Pull the imagepath for each tile
        nodeList = []
        # Indicate maximum column, row dimensions in the json
        pp.pprint(mapArray)
        maxCols = len(mapArray)
        maxRows = len(mapArray[0])
        mapDimsDict = {
            "mapDimensions": {
                "Xdim": maxCols,
                "Ydim": maxRows,
            }
        }
        nodeList.append(mapDimsDict)
        for colIndex in range(len(mapArray[0])):
            for rowIndex in range(len(mapArray)):
                # The map array contains the filepath for each tile's image
                filePath = mapArray[colIndex][rowIndex]
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
                    # Save all the information about the node into a structure
                    nodeData = {
                        "nodePosition": {
                            "X": colIndex,
                            "Y": rowIndex
                        },
                        "nodeStylePath": filePath,
                        "nodeStyleID": imageIndexArray[colIndex][rowIndex],
                        "nodeType": tileType,
                        "nodeEdges": tileEdgeDict
                    }
                    nodeList.append(nodeData)
        tileData = json.dumps(nodeList, indent=4)

        with open(path, "w") as fileOut:
            fileOut.write(tileData)
        # print(mapData)

    def Load(self, path):
        # Populate the mapArray and canvasArray based on data from json
        # Ingest the file object into a json object

        # Reference to the canvas object
        tileCanvas = self.parent.canvas.canvas
        # Reference to the tileSelector object
        tileSelector = self.parent.tileSelect
        # Reference to the toolSelector object
        toolSelector = self.parent.toolSelect

        # Clear the current map
        tileCanvas.delete('all')

        # Load the new map
        mapData = json.load(path)
        for tile in mapData:
            # print(tile)
            if "mapDimensions" in tile:
                # Extract map dimensions
                NewMapWidth = tile["mapDimensions"]["Xdim"]
                NewMapHeight = tile["mapDimensions"]["Ydim"]
                
                # Rebuild the arrays to the needed sizes
                self.generateNewMap(NewMapHeight, NewMapWidth)

                # Redraw gridlines
                tileCanvas.drawGridlines()
                # Refresh the canvas to show new data
                tileCanvas.update

                # print("Cleared map.")
            else:
                # Populate the map with tiles
                # Extract the tile position and image path
                tilePosition = tile["nodePosition"]
                tileID = tile["nodeStyleID"]
                
                # Set the tileSelector to match the desired tile appearance
                tileSelector.selectorCanvas.selectTile(tileID)

                # Set the current tool to "Paint" to use already-written methods
                toolSelector.selectorCanvas.paint()

                # Target the tile
                tileCanvas.selectedTile = (tilePosition["X"], tilePosition["Y"])

                # Draw the tile
                tileCanvas.setTile("click")
            # print(tile.nodePosition)
        # print(json.dumps(mapData, indent=4))