import os, sys, re, pdb, json

from pymongo import Connection
from pymongo.errors import ConnectionFailure, InvalidName

from bson.json_util import dumps

from lxml import etree

from mako.template import Template

# Database configuration & connection
try:
    c = Connection(host="0.0.0.0", port=27017)
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
database = c["restdb"]

def uri_magic_get(f):
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

def uri_magic_post(f):
        def new_f(uri,content):
            try:
                new_uri = uri.replace("/",".")
                if new_uri.startswith("."):
                    return f(new_uri[1:],content)
                else:
                    return f(new_uri,content)
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

def _create_document(form_content):
    document = dict()
    items = form_content.split("&")
    for item in items:
        key,value = item.split("=")
        value = value.replace("+"," ")
        document[key] = value
    return document

def _insert(uri,form_content):
    pdb.set_trace()
    member = database
    document = _create_document(form_content)
    for each in uri.split("."):
        member = getattr(member,each)
    member = getattr(member,'insert')
    member(document)
    
def _uri_to_etree(uri):
    root = None
    current_element = root
    for element in uri.split("."):
        if current_element is not None:
            current_element = etree.SubElement(current_element,element)
        else:
            root = etree.Element(element)
            current_element = root
    return root

def _populate_etree(element_tree,resources):
    for resource in resources:
        sub_element = etree.SubElement(element_tree, "resource")
        for key in resource.keys():
            if key == "_id":
                etree.SubElement(sub_element, "id").text = str(resource[key])
            else:
                etree.SubElement(sub_element, key).text = resource[key]
    return element_tree

@uri_magic_get
def get(uri):
    try:
        resources = query(uri)
        if resources:
            resource_xml = etree.tostring(_populate_etree(_uri_to_etree(uri),
                                                          resources),
                                          pretty_print=True,
                                          xml_declaration=True)
            template = Template(filename="/Users/jgoodell/code/python/rest-skunk-works/second_idea/templates/resources.html")
            return str(template.render(resources=resource_xml))
        else:
            return "<html>404 Not Found '%s'</html>" % uri
    except InvalidName, e:
        if uri == "":
            return open("index.html",'r').read()
        else:
            return "<html>404 Not Found '%s'</html>" % e

@uri_magic_post
def post(uri,form_content):
    _insert(uri,form_content)

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
