import ConfigParser
import sys, os

import BaseHTTPServer

from uri import UriDispatch

class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "TrivialHTTP/1.0"
    def do_GET(self):
        self.wfile.write("Hello World from '%s'" % self.path)
        self.wfile.close()
        self.send_header("Content-Type","application/text")
        self.send_response(200)

    do_PUT = do_POST = do_DELETE = do_GET

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    uri_dispatch = UriDispatch(config.get('general','uri_root'),
                               config.get('general','protocol_scheme'))
    run = True
    sys.stdout.write("Starting server..." + os.linesep)
    try:
        server = BaseHTTPServer.HTTPServer((config.get('general','host'),
                                            config.getint('general','port')), HTTPRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    sys.stdout.write(os.linesep + "Stopping server..." + os.linesep)
        
