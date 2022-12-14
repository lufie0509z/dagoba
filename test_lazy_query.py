from this import s
from unittest import TestCase

from .dagoba import Dagoba, LazyQuery
from . import fixtures

class LazyQueryTest(TestCase):
    def setUp(self):
        self.db = Dagoba(fixtures.nodes, fixtures.edges)
        self.q = self.db.query(eager = False)
        print('Testcase : test lazy query')

    def assert_nodes(self, nodes, pks):
        ids = set([x['_id'] for x in nodes])
        self.assertEqual(ids, set(pks))

    def test_grandkids(self):
        nodes = self.q.node(1).outcome().outcome().run()
        self.assert_nodes(nodes, [3, 4, 5, 6])

    def test_sons_father(self):
        nodes = self.q.node(1).outcome().income().outcome().run()
        self.assert_nodes(nodes, [2])

    def test_granddaughters(self):
        nodes = self.q.node(1).outcome().run()
        nodes = self.q.node(1).outcome().outcome(type_='daughter').run()
        self.assert_nodes(nodes, [6])

    def test_toms_sisters(self):
        nodes = self.q.node(3).outcome('sister').run()
        self.assert_nodes(nodes, [6])

    def test_toms_brothers_grandfater(self):
        nodes = self.q.node(3).outcome().income('son').income('son').run()
        self.assert_nodes(nodes, [1])

    def test_grandfater_unique(self):
        nodes = self.q.node(3).outcome().income('son').income('son').unique().run()
        self.assertEqual(1, len(nodes))
        self.assertEqual(1, Dagoba.pk(nodes[0]))

    def test_toms_sisters_brother(self):
        nodes =self.q.node(3).outcome('sister').outcome('brother').run()
        self.assert_nodes(nodes, [3, 4, 5])
    
    def test_take(self):
        nodes = self.q.node(1).outcome('son').outcome('son').take(1).run()
        pk = Dagoba.pk(nodes[0])
        self.assertIn(pk, [3, 4, 5])
    
    '''Test access efficiency'''
    def test_node_visits(self):
        self.db.reset_visits()
        eager_query = self.db.query(eager=True)
        eager_query.node(1).outcome('son').outcome('son').outcome('sister').take(1).run()
        eager_visits = self.db.get_visits()

        self.db.reset_visits()
        lazy_query = self.db.query(eager=False)
        nodes = lazy_query.node(1).outcome('son').outcome('son').outcome('sister').take(1).run()
        lazy_visits = self.db.get_visits()
        # print(lazy_visits, eager_visits)
        self.assertTrue(lazy_visits < eager_visits)

    def test_custom_query(self):
        def grandkids(self_):
            self_.outcome().outcome()
            return self_
        LazyQuery.grandkids = grandkids
        nodes = self.q.node(1).grandkids().run()
        self.assert_nodes(nodes, [3, 4, 5, 6])