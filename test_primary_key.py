from this import s
from unittest import TestCase

from .dagoba import Dagoba

class PrimaryKeyTest(TestCase):
    def setUp(self):
        self.db = Dagoba()
        self.pk1 = self.db.add_node({'name' : 'abc'})
        self.pk2 = self.db.add_node({'name' : 'xyz'})
        self.db.add_edge({'_from' : self.pk1, '_to' : self.pk2})
        print('Testcase: test primary key')

    
    def assert_item(self, items, **attrs):
        for item in items:
            for k, v in attrs.items():
                if item.get(k, None) != v:
                    continue
            return True
        self.fail(f'item with attrs({attrs}) not found')
    
    def get_item(self, items, **attrs):
        for item in items:
            for k, v in attrs.items():
                if item.get(k, None) == v:
                    return item
        self.fail(f'item with attrs({attrs}) not found')

    def test_nodes(self):
        nodes = list(self.db.nodes())
        self.assertEqual(2, len(nodes))
        self.assert_item(nodes, _id = 1, name = 'abc')
        self.assert_item(nodes, _id=  2, name = 'bar')
        self.assertIsNotNone(self.db.node(self.pk1))
        self.assertIsNotNone(self.db.node(self.pk2))


    def test_edges(self):
        edge = self.get_item(self.db.edges(), _from = self.pk1, _to = self.pk2)
        self.assertIsNotNone(edge)

