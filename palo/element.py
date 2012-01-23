from base import BasePaloObject

ELEMENT_TYPES = {'1':'NUMERIC', '2':'STRING', '4':'CONSOLIDATED'}

class Element(BasePaloObject):

    def __init__(self, c, dimension, data):
        self.c = c
        self.dimension = dimension
        self.id = data[0]
        self.name = data[1]
        self.position = data[2]
        self.level = data[3]
        self.indent = data[4]
        self.depth = data[5]
        self.type = ELEMENT_TYPES[data[6]]
        self.number_parents = data[7]
        self.parents = data[8]
        self.number_childern = data[9]
        self.childern = data[10]
        self.weights = data[11]