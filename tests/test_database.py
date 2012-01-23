import unittest, base

from palo import Connection

class DatabaseTest(base.BaseCase):
    
    def __init__(self, name='DatabaseTest'):
        base.BaseCase.__init__(self, name)
    
    def setUp(self):
        self.c = Connection(self.server, self.port, self.username, self.password)
        self.c.login()
    
    def teardown(self):
        self.c.logout()

    def test_00_list_cubes(self):
        demo = self.c.get_database_by_name('Demo')
        
        self.assertEqual(demo.load(), True)
        
        cubes = demo.get_cubes()
        
        self.assertEqual(cubes is not None, True)
        self.assertEqual(len(cubes.items()) > 0, True)
    
    def test_01_create_database(self):
        djw = self.c.get_database_by_name('djworth')
        if djw:
            djw.destroy()

        djw = self.c.create_database('djworth')
        
        self.assertEqual(djw is not None, True)
        self.assertEqual(djw.load(), True)
    
    def test_02_destroy_database(self):
        djw = self.c.get_database_by_name('djworth')
        
        self.assertEqual(djw.destroy(), True)
        
        djw = self.c.get_database_by_name('djworth')
        self.assertEqual(djw is None, True)
        