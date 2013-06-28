import os

def get(uri):
    try:
        opened_file = open(uri,'r')
        response = opened_file.read()
        opened_file.close()
        return response
    except IOError, e:
        return "404 Not Found '%s'" % e

def post(uri):
    try:
        new_file = open(uri,'w')
        new_file.write(uri)
        new_file.close()
    except IOError, e:
        return "403 Forbidden '%s'" % e
    return "200 OK"

def put(uri):
    try:
        if os.path.isfile(uri):
            opened_file = open(uri,'a')
            opened_file.write(uri)
            opened_file.close()
            return "200 OK"
        else:
            return "404 Not Found '%s'" % uri
    except IOError, e:
        return "403 Forbidden '%s'" % e

def delete(uri):
    try:
        os.remove(uri)
    except OSError, e:
        return "404 Not Found '%s'" % e
    return "200 OK"
