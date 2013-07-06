import os, sys, re, pdb, json

from pymongo import Connection
from pymongo.errors import ConnectionFailure, InvalidName

from bson.json_util import dumps

class NotFound(Exception):
    def __repr__(self):
        return "404 Not Found"
    
    def __int__(self):
        return 404

class Forbidden(Exception):
    def __repr__(self):
        return "403 Forbidden"
    
    def __int_(self):
        return 403

class InternalServerError(Exception):
    def __repr__(self):
        return "500 Internal Server Error"
    
    def __int__(self):
        return 500

# Database configuration & connection
try:
    c = Connection(host="0.0.0.0", port=27017)
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
database = c["restdb"]

def uri_magic(f):
        def new_f(uri):
            try:
                new_uri = uri.replace("/",".")
                if new_uri.startswith("."):
                    return f(new_uri[1:])
                else:
                    return f(new_uri)
            except AttributeError, e:
                return "<html>404 Not Found '%s'</html>" % e
        return new_f

def query(uri,args=dict()):
    "Function that walks the uri getting each dbh attribute and finally returning the result of the query as a list of BSON objects."
    response = list()
    member = database
    for each in uri.split('.'):
        member = getattr(member,each)
        try:
            for each in getattr(member,"find")(args):
                response.append(each)
        except TypeError:
            pass
    return response

@uri_magic
def get(uri):
    sys.stdout.write(uri)
    try:
        response = query(uri)
        if response:
            return dumps(response)
        else:
            return "<html>404 Not Found '%s'</html>" % uri
    except InvalidName, e:
        return "<html>404 Not Found '%s'</html>" % e

def post(uri,resource):
    try:
        new_file = open(uri,'w')
        new_file.write(uri)
        new_file.close()
        return "<resource><status>success</status><uri>%s</uri></resource>" % uri
    except IOError, e:
        return "<resource><status>failure</status><uri>%s</uri></resource>" % uri

def put(uri,resource):
    try:
        if os.path.isfile(uri):
            opened_file = open(uri,'a')
            opened_file.write(uri)
            opened_file.close()
            return "200 OK"
        else:
            #raise NotFound()
            return 404
    except IOError, e:
        #raise Forbidden()
        return 403

def delete(uri):
    try:
        os.remove(uri)
    except OSError, e:
        #return "404 Not Found '%s'" % e
        return 404
    return "200 OK"
