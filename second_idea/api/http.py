import os, sys, re

_uri_pattern = re.compile(r"^/(.+)")

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

def uri_magic(f):
    def new_f(uri):
        return f(_uri_pattern.match(uri).group(1))
    return new_f

# FIXME: These functions need to accept only
# hypertext and return only hypertext. The URI
# strings is okay by the raising of python error
# types is not.

@uri_magic
def get(uri):
    sys.stdout.write(uri)
    sys.stdout.write(os.getcwd())
    try:
        opened_file = open(uri,'r')
        response = opened_file.read()
        opened_file.close()
        return response
    except IOError, e:
        return ""

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
