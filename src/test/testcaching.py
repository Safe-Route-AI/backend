import unittest

import pytest

from src.utils.caching import load_graph


@pytest.mark.slow
class TestLoadGraph(unittest.TestCase):
    """
    These tests load the real Cairo GraphML from disk (310 MB) and are slow.
    Run with:  pytest --slow
    """

    def test_load_graph(self):
        graph = load_graph("Cairo, Egypt")

        self.assertGreater(graph.number_of_nodes(), 0)
        self.assertGreater(graph.number_of_edges(), 0)

    def test_graph_is_cached(self):
        graph1 = load_graph("Cairo, Egypt")
        graph2 = load_graph("Cairo, Egypt")

        self.assertIs(graph1, graph2)


if __name__ == "__main__":
    unittest.main()