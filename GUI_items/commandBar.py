# The command/menu bar at the top of most applications
import tkinter as tk
# For new map array generation
from GUI_items import mapDataArray, designCanvas
from tkinter import filedialog

class commandBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.parent.config(menu=self)
        self.file = FileCommands(self)

class FileCommands(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent, tearoff=0)
        self.parent = parent

        # Add menu elements
        self.add_command(label="New", command=self.FileNew)
        self.add_command(label="Open Map", command=self.OpenMap)
        self.add_command(label="Save Map", command=self.SaveMap)
        self.add_command(label="Quit", command=self.QuitOut)

        # Render the menu
        self.parent.add_cascade(label="File", menu=self)

    def FileNew(self):
        # Prompts the user to give dimensions of a new map and updates the mapData object
        self.dialogBox = tk.Toplevel(self.parent.parent)
        self.dialogBox.title("New Map Configuration")

        # Setup the inputs
        self.widthLabel = tk.Label(self.dialogBox, text="Width: ", font=('Calibri 10'))
        self.widthEntry = tk.Entry(self.dialogBox, width=30)
        self.heightLabel = tk.Label(self.dialogBox, text="Height: ", font=('Calibri 10'))
        self.heightEntry = tk.Entry(self.dialogBox, width=30)

        # Render the inputs
        self.widthLabel.grid(row=0, column=0)
        self.widthEntry.grid(row=0, column=1)
        self.heightLabel.grid(row=1, column=0)
        self.heightEntry.grid(row=1, column=1)

        # Confirm button
        self.Button = tk.Button(self.dialogBox, text = "Make New Map", width = 25, command=self.NewMap)
        self.Button.grid(row=2, column=1)
        print("new file")

    def NewMap(self):
        # Grab the entry field values
        NewMapWidth = self.widthEntry.get()
        NewMapHeight = self.heightEntry.get()

        # Clear the canvas
        self.parent.parent.canvas.canvas.delete('all')

        # Update objects
        self.parent.parent.mapData = mapDataArray(self.parent, (int(NewMapWidth), int(NewMapHeight)))
        self.parent.parent.canvas.canvas = designCanvas(self.parent.parent.canvas)

        # Refresh the canvas to show new data
        self.parent.parent.canvas.canvas.update

        # Close the new map dialog
        self.dialogBox.destroy()

    def OpenMap(self):
        print("open map")

    def SaveMap(self):
        saveType = tk.IntVar()

        # Create dialog box
        self.dialogBox = tk.Toplevel(self.parent.parent)
        self.dialogBox.title("Choose save method")

        # Option buttons
        button1 = tk.Radiobutton(self.dialogBox, text="Save only the region containing tiles", variable=saveType, value=1)
        button2 = tk.Radiobutton(self.dialogBox, text="Save entire map including empty edges", variable=saveType, value=2)
        button1.pack(anchor = tk.W)
        button2.pack(anchor = tk.W)
        button1.select()

        # Confirm button
        confirm = tk.Button(self.dialogBox, text="Ok", width=5, command=lambda i=saveType: self.Save(i))
        confirm.pack()
        print("save map")

    def Save(self, saveType):
        FTypes = [("Comma Separated", ".csv")]
        path = tk.filedialog.asksaveasfile(title="Save Map", filetypes = FTypes, defaultextension = FTypes)
        self.parent.parent.mapData.Save(path, saveType)

    def QuitOut(self):
        print("quit")
        
        