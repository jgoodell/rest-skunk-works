import json, lxml
from pprint import pprint

def create_resource(hypertext):
    print('here')
    try:
        json_data = json.loads(hypertext)
        return True
    except ValueError, e:
        pprint(dir(lxml))
        xml_data = lxml.etree.fromstring(hypertext)
        return False
