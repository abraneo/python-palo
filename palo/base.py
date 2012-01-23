import csv, urllib, httplib
from StringIO import StringIO

import logging

LOG_FILENAME = 'palo-request.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

class BasePaloObject(object):

    def execute(self, server, port, action, **params):
        h = httplib.HTTPConnection(server, port)

        logging.info("REQUESTING INFO: %s?%s" % (action, urllib.urlencode(params)))
        
        h.request("GET", "%s?%s" % (action, urllib.urlencode(params)), headers={})
        r = h.getresponse()
        payload = r.read()
        
        logging.info("RESPONSE: %s" % payload)
        
        if r.status != 200:
            raise Exception("Error: %s returned (%d): %s" % (action, r.status, payload))


        return csv.reader(StringIO(payload), delimiter=';')