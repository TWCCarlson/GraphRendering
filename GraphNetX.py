import networkx as netx
import pprint

pretty_print = pprint.PrettyPrinter()

# Define FloorTile class
class FloorTile:
    # Instantiations should provide a coordinate location
    # As well as the function of the tile (open space, rest station, )
    def __init__(self, TileID, Coords, TileType):
        self.TileID = TileID
        self.Xpos = Coords[0]
        self.Ypos = Coords[1]
        self.TileType = TileType

# Instantiate the graph
FloorMap = netx.Graph()

# Node styleguide
FloorMap.add_node('1', Coords=(0,0), TileType='Open')
FloorMap.add_node('2', Coords=(1,0), TileType='Open')
FloorMap.add_node('3', Coords=(0,1), TileType='Open')
FloorMap.add_node('4', Coords=(1,1), TileType='Open')

# Nicer print statement
pretty_print.pprint(dict(FloorMap.nodes.data()))

for line in netx.generate_adjlist(FloorMap):
    print(line)

    
