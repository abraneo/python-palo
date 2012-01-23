from base import BasePaloObject
from cube import Cube

DATABASE_STATUS = {'0':'unloaded', '1':'system', '2':'changed'}
DATABASE_TYPES = {'0':'normal', '1':'system', '3':'user info'}

DATABASE_TYPE_NORMAL = '0'
DATABASE_TYPE_SYSTEM = '1'
DATABASE_TYPE_USERINFO = '3'

class Database(BasePaloObject):

    def __init__(self, c, data):
        self.c = c
        self.id = data[0]
        self.name = data[1]
        self.number_of_dimensions = data[2]
        self.number_of_cubes = data[3]
        self.status = DATABASE_STATUS[data[4]]
        self.type = DATABASE_TYPES[data[5]]
        self.token = data[6]

    def __str__(self):
        return 'id: %s, name: %s, # of dimensions: %s, # of cubes: %s, status: %s, type: %s' % (self.id, 
                                                                                                self.name, 
                                                                                                self.number_of_dimensions, 
                                                                                                self.number_of_cubes, 
                                                                                                self.status, 
                                                                                                self.type)

    def load(self):
        results = self.c._send('/database/load', database=self.id)

        first = results.next()

        #1 means OK it's loaded
        return first[0] == '1'

    def destroy(self):
        results = self.c._send('/database/destroy', database=self.id)
        first = results.next()

        #1 means OK it's loaded
        return first[0] == '1'

    def get_info(self):
        results = self.c._send('/database/info', database=self.id)

        info = []

        for row in results:
            info.append(row)

        return info
    
    def get_dimesions(self, normal=True, system=False, attribute=False, info=False):

        database = 1 if database else 0
        show_normal = 1 if normal else 0
        show_system = 1 if system else 0
        show_attribute = 1 if attribute else 0
        show_info = 1 if info else 0
        
        reader = self.c._send('/database/dimensions', 
                                database=self.id, 
                                show_normal=show_normal, 
                                show_system=show_system, 
                                show_attribute=show_attribute,
                                show_info=show_info)
        
        data = {}
        for row in reader:
            data[row[1]] = Dimesion(self.c, self, row)

        return data

    def get_cubes(self, normal=True, system=False, attribute=False, info=False, gpu=False):
        """
        Returns the list of cubes.
        """

        show_normal = 1 if normal else 0
        show_system = 1 if system else 0
        show_attribute = 1 if attribute else 0
        show_info = 1 if info else 0
        show_gputype = 1 if gpu else 0

        reader = self.c._send('/database/cubes', 
                                database=self.id, 
                                show_normal=show_normal, 
                                show_system=show_system, 
                                show_attribute=show_attribute,
                                show_info=show_info,
                                show_gputype=show_gputype)

        data = {}
        for row in reader:
            data[row[1]] = Cube(self.c, self, row)

        return data

    def rename(self, new_name):
        results = self.c._send('/database/rename', 
                                database=self.id, 
                                new_name=new_name)

        data = []

        for row in results:
            data.append(row)

        return data

    def save(self):
        results = self.c._send('/database/save', database=self.id)

        first = results.next()

        #1 means OK it's loaded
        return first[0] == '1'

    def unload(self):
        results = self.c._send('/database/unload', database=self.id)

        first = results.next()

        #1 means OK it's loaded
        return first[0] == '1'

    def create_dimension(self, name, type=0):

        reader = self.c._send('/dimension/create', 
                                database=self.id, 
                                new_name=name, 
                                type=type)

        if len(reader) > 0:
            return Dimesion(self.c, self, reader.next())

        return None