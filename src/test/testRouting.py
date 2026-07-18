"""Tests for src.utils.routing.get_k_shortest_paths (4.1)."""

import unittest

import networkx as nx

from src.utils.routing import get_k_shortest_paths


def _build_synthetic_graph() -> nx.MultiDiGraph:
    """
    A --- B --- C
          |
          D
    """
    g = nx.MultiDiGraph()
    g.graph["crs"] = "epsg:4326"
    nodes = {
        "A": (30.0400, 31.2300),
        "B": (30.0410, 31.2310),
        "C": (30.0420, 31.2320),
        "D": (30.0400, 31.2310),
    }
    for node_id, (lat, lon) in nodes.items():
        g.add_node(node_id, y=lat, x=lon)

    g.add_edge("A", "B", key=0, length=100, name="Tahrir Street")
    g.add_edge("B", "A", key=0, length=100, name="Tahrir Street")
    g.add_edge("B", "C", key=0, length=120, ref="R12")
    g.add_edge("C", "B", key=0, length=120, ref="R12")
    g.add_edge("B", "D", key=0, length=90)
    g.add_edge("D", "B", key=0, length=90)
    g.add_edge("A", "D", key=0, length=150, name="Nile Corniche")
    g.add_edge("D", "A", key=0, length=150, name="Nile Corniche")
    return g


class TestGetKShortestPaths(unittest.TestCase):
    def setUp(self):
        self.graph = _build_synthetic_graph()

    def test_returns_shortest_path_first(self):
        paths = get_k_shortest_paths(self.graph, "A", "C", k=1)
        self.assertEqual(paths[0], ["A", "B", "C"])

    def test_returns_up_to_k_paths_in_increasing_length(self):
        paths = get_k_shortest_paths(self.graph, "A", "C", k=3)
        self.assertGreaterEqual(len(paths), 1)

        def path_len(path):
            total = 0
            for u, v in zip(path, path[1:]):
                total += min(
                    data["length"] for data in self.graph.get_edge_data(u, v).values()
                )
            return total

        actual_lengths = [path_len(p) for p in paths]
        self.assertEqual(actual_lengths, sorted(actual_lengths))

    def test_invalid_k_raises(self):
        with self.assertRaises(ValueError):
            get_k_shortest_paths(self.graph, "A", "C", k=0)

    def test_unknown_node_raises(self):
        with self.assertRaises(ValueError):
            get_k_shortest_paths(self.graph, "A", "Z", k=1)

    def test_no_path_raises(self):
        g = self.graph.copy()
        g.add_node("Island", y=0, x=0)
        with self.assertRaises(nx.NetworkXNoPath):
            get_k_shortest_paths(g, "A", "Island", k=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)