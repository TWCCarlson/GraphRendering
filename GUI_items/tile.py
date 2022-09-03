# This class is the fundamental item placed on the map

# Import ability to handle images with Pillow
import PIL.ImageTk
import PIL.Image

class Tile(): #class structure to hold images
    def __init__(self, path, size):
        self.size = size
        self.path = path
        self.image  = PIL.Image.open(open(path, 'rb')) #open a regular PIL image
        self.image = self.image.resize((self.size, self.size)) #resize the image
        self.image = PIL.ImageTk.PhotoImage(self.image) #convert image to a tk displayable image