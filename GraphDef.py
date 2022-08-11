
from collections import defaultdict

class Graph(object):
    """ Graph data structure
        Undirected by default
        Adjacency list style """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add many connections (tuple pairs) """
        for firstNode, secondNode in connections:
            self.add_edge(firstNode, secondNode)

    def add_edge(self, firstNode, secondNode):
        """ Add a single connection (tuple pair) """
        self._graph[firstNode].add(secondNode)

        # If the graph is undirected (default), then a matching connection in the opposite direction is needed
        if not self._directed:
            self._graph[secondNode].add(firstNode)
        # return "Added connection between '" + firstNode + "' and '" + secondNode + "'"

    def adjacent(self, firstNode, secondNode):
        """ Report whether an edge exists from firstNode to secondNode """
        # Graph is in set format, key is in dict, value is in key's set
        return firstNode in self._graph and secondNode in self._graph[firstNode]

    def neighbors(self, node):
        """ List all nodes which have an edge connection to this node """
        return self._graph[node]

    def remove_connections(self, connections):
        """ Remove many connections (tuple pairs) """
        for firstNode, secondNode in connections:
            self.remove_edge(firstNode, secondNode)

    def remove_edge(self, firstNode, secondNode):
        """ Remove a connection between two nodes """
        self._graph[firstNode].remove(secondNode)
        # If the graph is undirected (default), then a matching connection in the opposite direction needs to be removed as well
        if not self._directed:
            self._graph[secondNode].remove(firstNode)



# Test code

# import pprint
# connections = [((1,1), (1,2)), ((1,1), (2,1)), ((1,2), (1,3)), 
#                 ((1,2), (2,2)), ((2,1), (2,2)), ((2,1), (3,1))]
# g = Graph(connections)
# pretty_print = pprint.PrettyPrinter()
# pretty_print.pprint(g._graph)
# g.add_edge((2,2), (2,3))
# g.add_edge((2,2), (3,2))
# pretty_print.pprint(g._graph)
# g.add_connections([((2,3), (3,1)), ((3,2), (1,3))])
# pretty_print.pprint(g._graph)
# g.remove_connections([((2,2), (1,2)), ((2,2), (2,1))])
# pretty_print.pprint(g._graph)