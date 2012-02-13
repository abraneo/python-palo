import csv
import logging
import urllib
import requests

from StringIO import StringIO

LOG_FILENAME = 'palo-request.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

class BasePaloObject(object):

    def execute(self, server, port, action, **params):
        action = "http://%(server)s:%(port)s%(action)s?%(params)s" % {  'server':server, 
                                                                        'port':port, 
                                                                        'action':action,
                                                                        'params':urllib.urlencode(params)}

        logging.info("REQUESTING INFO: %s" % action)
        
        r = requests.get(action)
        payload = r.text
        
        logging.info("RESPONSE: %s" % payload)
        
        if r.status_code != requests.codes.ok:
            raise Exception("Error: %s returned (%d): %s" % (action, r.status_code, payload))

        return csv.reader(StringIO(payload), delimiter=';')