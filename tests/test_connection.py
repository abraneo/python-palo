import unittest, os, base

from palo import Connection

class ConnectionTest(base.BaseCase):
    
    def __init__(self, name='ConnectionTest'):
        base.BaseCase.__init__(self, name)
    
    def setUp(self):
        self.c = Connection(self.server, self.port, self.username, self.password)
        self.c.login()
    
    def teardown(self):
        self.c.logout()

    def test_00_login(self):
        s = Connection(self.server, self.port, self.username, self.password)

        session = s.login()

        self.assertEqual(session.get('session_id', None) is not None, True)
        self.assertEqual(len(session.get('session_id', '')) > 0, True)
        self.assertEqual(session.get('timeout', 0) != 0, True)

    def test_01_logout(self):
        c = Connection(self.server, self.port, self.username, self.password)

        session = c.login()
        self.assertEqual(c.logout(), True)

    def test_02_info(self):

        data = self.c.get_info()
        
        self.assertEqual(data is not None, True)
        self.assertEqual(len(data.keys()), 6)
        self.assertEqual(len(data.values()), 6)

    def test_03_databses(self):
        data = self.c.get_databases()

        self.assertEqual(len(data.keys()) > 0, True)

    def test_04_save(self):
        self.assertEqual(self.c.save(), True)
    
    """
    def test_05_shutdown(self):
        self.assertEqual(self.c.shutdown(), True)
    """
    
    def test_06_load(self):
        self.assertEqual(self.c.load(), True)

    def test_07_database_by_name(self):
        demo = self.c.get_database_by_name('Demo')
        
        self.assertEqual(demo is not None, True)
        self.assertEqual(demo.name.lower(), 'Demo'.lower())
        
        demo = self.c.get_database_by_name('demo')
        self.assertEqual(demo is not None, True)
        
        demo = self.c.get_database_by_name('DemoASDFADFSADSFADFADFS')
        self.assertEqual(demo is None, True)
        