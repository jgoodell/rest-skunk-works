import ConfigParser
import sys, os

import BaseHTTPServer

from uri import UriDispatch

class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    pass

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    uri_dispatch = UriDispatch(config.get('general','uri_root'),
                               config.get('general','protocol_scheme'))
    run = True
    sys.stdout.write("Starting server..." + os.linesep)
    while run:
        try:
            sys.stdout.write(uri_dispatch.receive_request(raw_input(),"DELETE") + os.linesep)
        except KeyboardInterrupt:
            run = False
    sys.stdout.write(os.linesep + "Stopping server..." + os.linesep)
        
