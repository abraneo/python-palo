import csv
import hashlib
import urllib
import urllib2

from base import BasePaloObject
from database import Database, DATABASE_TYPE_NORMAL

class Connection(BasePaloObject):
    
    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
    
    def get_info(self):
        """
        Returns information about the server, i. e. its version number.
        """
        reader = self._send('/server/info')
        first = reader.next()

        data = {'major_version': first[0],  #major version of the server
                'minor_version': first[1],  #minor version of the server
                'bugfix_version': first[2], #bugfix level of the server
                'build_number': first[3],   #build number of the server
                'encryption': first[4],     #0 for none, 1 for optional, 2 for required
                'https_port': first[5],     #the corresponding HTTPS port or 0 if HTTPS is not supported
            }
        
        return data
    
    def create_database(self, name, type=DATABASE_TYPE_NORMAL):
    
        results = self._send('/database/create', new_name=name, type=type)
        first = results.next()
        
        return self.get_database_by_id(first[0])
        
    
    def get_databases(self, load=True):
        """
        Possible status of a database
          * unloaded: the saved databases is not loaded to memory. Number of of dimensions and cubes are not set.
          * loaded: the database is loaded into memory and no modifications have been made since the last save.
          * changed: the database is loaded into memory and modifications exists since the last save. Or the database is newly created.
        """
        reader = self._send('/server/databases')
        
        data = {}
        for row in reader:
            db = Database(self, row)
            
            if load:
                db.load()
            
            data[row[0]] = db

        return data
    
    def get_database_by_name(self, name):
        databases = self.get_databases()
        
        for k,v in databases.items():
            if v.name.lower() == name.lower():
                return v
        
        return None
    
    def get_database_by_id(self, database_id):
        databases = self.get_databases()
        
        return databases.get(database_id, None)
    
    def login(self, extern_password=None):
        """
        The session identifier (sid) is used to identify a connection to the palo server. Therefore the session identifier has to be appended to each request (except /server/login and /server/info request). 
        If no request is made using a session identifier for some time, the session will timeout and becomes invalid. A new session identifier has to be requested in this case.
        """
        md5 = hashlib.md5()
        md5.update(self.password)
        password = md5.hexdigest()

        reader = self._send('/server/login', requires_auth=False, user=self.username, password=password, extern_password=extern_password)
        first = reader.next()
        
        data = {'session_id':first[0], 'timeout':first[1]}
        
        self.session_id = data['session_id']
        
        return data

    def logout(self):
        """
        The session identifier can no longer be used after this request. It becomes invalid.
        """
        reader = self._send('/server/logout')
        first = reader.next()
        
        return first[0] == "1"

    def load(self):
        """
        Reloads the server from disk
        """
        reader = self._send('/server/load')
        first = reader.next()

        return first[0] == "1"
    
    def get_license(self):
        """
        Shows information about the server license.
        """
        reader = self._send('/server/license')
        
        return reader

    def save(self):
        """
        This request saves the server data, i. e. identifiers and database names, to disk. To save database and cube data use the requests "/database/save" and "/cube/save".
        """
        reader = self._send('/server/save')
        first = reader.next()

        return first[0] == "1"

    def shutdown(self):
        """
        Shuts down the server
        """
        reader = self._send('/server/shutdown')
        first = reader.next()

        return first[0] == "1"
    
    def change_password(self, new_password):
        results = self.c._send('/server/change_password', password=new_password)
        
        first = results.next()
        
        #1 means OK it's loaded
        return first[0] == '1'
    
    def _send(self, action, requires_auth=True, **params):
    
        if requires_auth:
            if not hasattr(self, 'session_id'):
                raise Exception("ERROR: %s action requires authenication" % action)
            else:
                return self.execute(self.server, self.port, action, sid=self.session_id, **params)
        else:
            return self.execute(self.server, self.port, action, **params)

if __name__ == '__main__':
    c = Connection('localhost', 7777, 'admin', 'admin')

    print c.get_info()
    license = c.get_license()
    for row in license:
        print row

    print c.login()
    
    databases = c.get_databases()
    for k, v in databases.items():
        print v
    
    print c.logout()
    