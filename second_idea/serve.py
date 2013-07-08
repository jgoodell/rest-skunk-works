import ConfigParser
import sys, os, pdb
from pprint import pprint

from twisted.web import resource, server
from twisted.internet import reactor

from uri import UriDispatch
from api.http import get, post, put, delete


class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        request.setResponseCode(200)
        request.setHeader("Content-Type","text/html")
        return get(request.uri)

    def render_PUT(self, request):
        return "<html>PUT</html>"

    def render_POST(self, request):
        return post(request.uri,request.content.read())

    def render_DELETE(self, request):
        return "<html>DELETE</html>"


if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    uri_dispatch = UriDispatch(config.get('general','uri_root'),
                               config.get('general','protocol_scheme'))
    run = True
    sys.stdout.write("Starting server..." + os.linesep)
    host = config.get('general','host')
    port = config.getint('general','port')
    site = server.Site(Simple())
    reactor.listenTCP(port,site)
    reactor.run()
    sys.stdout.write(os.linesep + "Stopping server..." + os.linesep)
        
