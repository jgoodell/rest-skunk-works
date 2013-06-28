from unittest import TestCase

from rest_api.create import create_resource

class CreateTestCase(TestCase):
    def setUp(self):
        self.json_hypertext = '{"authors":{"1":{"firstname":"George","lastname":"Orwell"},"2":{"firstname":"Stephen","lastname":"King"}}}'
        self.simple_json = '{"name":"jason","age":32}'

        self.xml_hypertext = '''<authors>
        <author>
        <firstname>George</firstname>
        <lastname>Orwell</lastname>
        </author>
        <author>
        <firstname>Stephen</firstname>
        <lastname>King</lastname>
        </author>
        </authors>'''

    def tearDown(self):
        pass

    def test_create_json(self):
        self.assertTrue(create_resource(self.json_hypertext))

    def test_create_xml(self):
        self.assertTrue(create_resource(self.xml_hypertext))
