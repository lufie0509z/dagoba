from unittest import TestCase
from .dagoba import Dagoba

class DbModelTest(TestCase):
    nodes = [{'_id' : 1, 'name' : 'abc'}, {'_id': 2, 'name' : 'xyz'},]
    edges = [{'_in' : 3, '_out': 2},]
    
    def setUp(self):
        self.db = Dagoba(self.nodes, self.edges)
    
    def assert_item(self, items, **attrs):
        for item in items:
            for k, v in attrs.items():
                if item.get(k, None) != v:
                    continue
            return True
        self.fail(f'item with attrs({attrs}) not found')

    def test_nodes(self):
        nodes = list(self.db.nodes())
        self.assertEqual(2, len(nodes))
        self.assert_item(nodes, _id = 1, name = 'abc')
        self.assert_item(nodes, _id=  2, name = 'bar')
        
    def test_edges(self):
        edges = list(self.db.edges())
     
        self.assertEqual(1, len(edges))
        self.assert_item(edges, _in = 1, _out = 2)
    

