from base import BasePaloObject

CUBE_STATUS = {'0':'unloaded', '1':'system', '2':'changed'}
CUBE_TYPE = {'0':'normal', '1':'system', '2':'attribute', '3':'user info', '4':'gpu type'}

class Cube(BasePaloObject):
    
    def __init__(self, c, database, data):
        self.c = c
        self.database = database
        self.id = data[0]
        self.name = data[1]
        self.number_of_dimensions = data[2]
        self.dimensions = data[3]
        self.number_cells = data[4]
        self.number_filled_cells = data[5]
        self.status = CUBE_STATUS[data[6]]
        self.type = CUBE_TYPE[data[7]]
        self.token = data[8]