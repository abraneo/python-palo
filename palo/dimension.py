from base import BasePaloObject
from cube import Cube
from element import Element

DIMESION_STATUS = {'0':'unloaded', '1':'system', '2':'changed'}
DIMESION_TYPE = {'0':'normal', '1':'system', '2':'attribute', '3':'user info'}

class Dimesion(BasePaloObject):

    def __init__(self, c, database, data):
        self.c = c
        self.database = database
        self.id = data[0]
        self.name = data[1]
        self.number_elements = data[2]
        self.maximum_level = data[3]
        self.maximum_indent = data[4]
        self.maximum_depth = data[5]
        self.status = DIMESION_TYPE[data[6]]
        self.attributes_dimension = data[7]
        self.attributes_cube = data[8]
        self.rights_cube = data[9]
        self.dimension_token = data[10]
    
    
    def get_cubes(self, normal=True, system=False, attribute=False, info=False, gpu=False):
        """
        Returns the list of cubes.
        """

        show_normal = 1 if normal else 0
        show_system = 1 if system else 0
        show_attribute = 1 if attribute else 0
        show_info = 1 if info else 0
        show_gputype = 1 if gpu else 0

        reader = self.c._send('/dimesion/cubes', 
                                database=self.database.id, 
                                dimesion=self.id,
                                show_normal=show_normal, 
                                show_system=show_system, 
                                show_attribute=show_attribute,
                                show_info=show_info,
                                show_gputype=show_gputype)

        data = {}
        for row in reader:
            data[row[1]] = Cube(self.c, self, row)

        return data
    
    def clear(self):
        
        reader = self.c._send('/dimesion/clear', 
                                database=self.database.id, 
                                dimesion=self.id)

        if len(reader) > 0:
            return Dimesion(self.c, self.database, reader.next())

        return None
    
    def destroy(self):
        results = self.c._send('/dimesion/destroy', database=self.database.id, dimesion=self.id)

        first = results.next()

        #1 means OK it's loaded
        return first[0] == '1'

    def get_element(self, position):
        reader = self.c._send('/dimesion/element', 
                                database=self.database.id, 
                                dimesion=self.id,
                                position=position)

        if len(reader) > 0:
            return Element(self.c, self, reader.next())

        return None

    def get_elements(self):
        reader = self.c._send('/dimesion/elements', 
                                database=self.database.id, 
                                dimesion=self.id)

        data = {}
        for row in reader:
            data[row[1]] = Element(self.c, self, row)

        return data

    def info(self):
        reader = self.c._send('/dimesion/info', 
                                database=self.database.id, 
                                dimesion=self.id)


        first = reader.next()

        return Dimension(self.c, self.database, first)

    def rename(self, new_name):
        reader = self.c._send('/dimesion/rename', 
                                database=self.database.id, 
                                dimesion=self.id,
                                new_name=new_name)


        first = reader.next()
        
        d = Dimension(self.c, self.database, first)
        self.name = d.name
        
        return d

    def filter(self):
        """
        Not implemented yet
        """
        raise Exception('Not Implemented Yet.')
        