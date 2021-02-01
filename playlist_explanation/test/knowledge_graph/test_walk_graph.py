import unittest
import networkx as nx
from unittest.mock import patch
from src.knowledge_graph.walk_graph import find_segues


class TestWalkGraph(unittest.TestCase):

    def _resolve_compare_function(self, *args):
        def func(n1, n2):
            if n1['value'] == n2['value']:
                return True
            else:
                return False
        return func

    @patch('src.knowledge_graph.walk_graph.resolve_compare_function')
    def test_walk_graph(self, mock_resolve_compare_function):
        mock_resolve_compare_function.side_effect = self._resolve_compare_function
        g1 = nx.DiGraph()

        g1.add_node('a')
        g1.nodes['a']['type'] = ['artist_uri_dbpedia']
        g1.nodes['a']['value'] = 'a'

        g1.add_node('b')
        g1.nodes['b']['type'] = ['artist_uri_dbpedia']
        g1.nodes['b']['value'] = 'b'

        g1.add_node('c')
        g1.nodes['c']['type'] = ['album_name']
        g1.nodes['c']['value'] = 'c'

        g1.add_node('d')
        g1.nodes['d']['type'] = ['album_name']
        g1.nodes['d']['value'] = 'd'

        g1.add_node('e')
        g1.nodes['e']['type'] = ['artist_name']
        g1.nodes['e']['value'] = 'e'

        g2 = nx.DiGraph()

        g2.add_node('a')
        g2.nodes['a']['type'] = ['artist_uri_dbpedia']
        g2.nodes['a']['value'] = 'a'

        g2.add_node('c')
        g2.nodes['c']['type'] = ['album_name', 'artist_uri_dbpedia']
        g2.nodes['c']['value'] = 'c'

        g2.add_node('d')
        g2.nodes['d']['type'] = ['artist_uri_dbpedia']
        g2.nodes['d']['value'] = 'd'

        g2.add_node('e')
        g2.nodes['e']['type'] = []
        g2.nodes['e']['value'] = 'e'

        matches = find_segues_to_common_nodes(g1, g2)
        self.assertEqual(matches, [('a', 'a'),
                                   ('c', 'c')])
