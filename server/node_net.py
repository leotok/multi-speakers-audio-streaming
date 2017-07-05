from collections import defaultdict

class Node(object):

    def __init__(self, number, name=""):

        self.number = number
        if name:
            self.name = name
        else:
            self.name = "node" + str(number)

    def __str__(self):
        return "Node " + str(self.number) + ": " + self.name


class NodeNet(object):

    def __init__(self):
        self.nodes = dict()
        self.graph = defaultdict(set)

    def add_node(self, number, name):
        node = Node(number, name)
        self.nodes[number] = node
        self.graph[number] = set()
        return node

    def get_node(self, number):
        try:
            return self.nodes[int(number)]
        except:
            return None

    def get_nodes(self):
        return self.nodes.values()

    def add_neighbours_to_node(self, node_number, neighbours):
        node = self.get_node(node_number)

        for n in neighbours:
            self.graph[node.number].add(n)

