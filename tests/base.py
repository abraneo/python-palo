import unittest, os

SERVER = os.environ.get('PALO_SERVER', 'localhost')
PORT = os.environ.get('PALO_PORT', '7777')
USERNAME = os.environ.get('PALO_USERNAME', 'admin')
PASSWORD = os.environ.get('PALO_PASSWORD', 'admin')

class BaseCase(unittest.TestCase):
    
    def __init__(self, name):
        unittest.TestCase.__init__(self, name)
        self.server = SERVER
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD