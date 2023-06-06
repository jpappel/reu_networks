import unittest
import networkx as nx
import p_connectivity as p_conn
import properties
from itertools import product

class LocalCircumferenceEdges(unittest.TestCase):
    def setUp(self):
        MAX_PART_A = 3
        MAX_PART_B = 8
        assert MAX_PART_A <= MAX_PART_B
        self.parts = []
        for i in range(1,MAX_PART_A):
            for j in range(i,MAX_PART_B):
                self.parts.append((i,j))

    def test_circumference_too_large(self):
        for part_a, part_b in self.parts:
            g = nx.complete_bipartite_graph(part_a, part_b)
            for l in range(2*part_a + 1, 3*part_a + 1):
                with self.subTest(l=l):
                    has_l_circ = properties.has_l_circ(l)
                    comp_p_edge_conn = p_conn.component_p_edge_connectivity(g, has_l_circ)
                    self.assertEqual(0, len(comp_p_edge_conn[0]))

    def test_equitable(self):
        for part_a, part_b in filter(lambda ab : ab[0] == ab[1], self.parts):
            g = nx.complete_bipartite_graph(part_a, part_b)
            l = 2*part_a
            with self.subTest(l=l):
                has_l_circ = properties.has_l_circ(l)
                comp_p_edge_conn = p_conn.component_p_edge_connectivity(g, has_l_circ)
                self.assertEqual(part_a - 1, len(comp_p_edge_conn[0]))

    def test_less_than_equitable(self):
        for part_a, part_b in filter(lambda ab : ab[0] < ab[1], self.parts):
            g = nx.complete_bipartite_graph(part_a,part_b)
            for l in range(3,2*part_a + 1):
                with self.subTest(l=l):
                    has_l_circ = properties.has_l_circ(l)
                    comp_p_edge_conn = p_conn.component_p_edge_connectivity(g, has_l_circ)
                    self.assertEqual(part_a, len(comp_p_edge_conn[0]))


if __name__ == "__main__":
    unittest.main()
