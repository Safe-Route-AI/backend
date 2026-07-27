"""Tests for src.utils.lookup.get_street_name and location_to_street (4.2, 4.3)."""

import unittest
from unittest.mock import patch

import networkx as nx
# pyrefly: ignore [missing-import]
import pytest

from src.utils.lookup import (
    get_street_name,
    location_to_street,
    get_pois,
    coords_to_street,
)


def _build_synthetic_graph() -> nx.MultiDiGraph:
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


class TestGetStreetName(unittest.TestCase):
    def test_returns_name_when_present(self):
        self.assertEqual(get_street_name({"name": "Tahrir Street"}), "Tahrir Street")

    def test_falls_back_to_ref(self):
        self.assertEqual(get_street_name({"ref": "R12"}), "R12")

    def test_falls_back_to_unnamed(self):
        self.assertEqual(get_street_name({}), "Unnamed Road")
        self.assertEqual(get_street_name(None), "Unnamed Road")

    def test_handles_list_valued_name(self):
        self.assertEqual(
            get_street_name({"name": ["6th of October Bridge", "Corniche"]}),
            "6th of October Bridge",
        )


class TestLocationToStreet(unittest.TestCase):
    def setUp(self):
        self.graph = _build_synthetic_graph()

    def test_nearest_point_on_named_edge(self):
        street = location_to_street(self.graph, 30.0405, 31.2305)
        self.assertEqual(street, "Tahrir Street")

    def test_nearest_point_on_ref_only_edge(self):
        street = location_to_street(self.graph, 30.0415, 31.2315)
        self.assertEqual(street, "R12")

    def test_invalid_coordinates_raise(self):
        with self.assertRaises(ValueError):
            location_to_street(self.graph, 999, 31.23)


# Shahd part (get_pois, coords_to_street)

class TestGetPois(unittest.TestCase):
    """
    Fast unit test: mocks the OSM network call.
    Run the real network version with:  pytest --slow
    """

    @patch("src.utils.lookup.ox.features.features_from_point")
    def test_get_pois_returns_dict_with_expected_keys(self, mock_features):
        import pandas as pd

        # Return a minimal GeoDataFrame with one police entry
        mock_features.return_value = pd.DataFrame(
            {"amenity": ["police"], "railway": [None]}
        )

        pois = get_pois(30.0444, 31.2357)

        self.assertIsInstance(pois, dict)
        self.assertIn("hospital", pois)
        self.assertIn("restaurant", pois)
        self.assertIn("police", pois)
        self.assertIn("metro", pois)
        self.assertIn("pharmacy", pois)

    def test_invalid_coordinates_raise(self):
        with self.assertRaises(ValueError):
            get_pois(999, 31.23)


@pytest.mark.slow
class TestGetPoisIntegration(unittest.TestCase):
    """Real network call – skipped by default. Run with: pytest --slow"""

    def test_get_pois_real(self):
        pois = get_pois(30.0444, 31.2357)
        self.assertIsInstance(pois, dict)
        self.assertIn("hospital", pois)
        self.assertIn("restaurant", pois)
        self.assertIn("police", pois)
        self.assertIn("metro", pois)
        self.assertIn("pharmacy", pois)


class TestCoordsToStreet(unittest.TestCase):
    """
    Fast unit tests: mock load_graph so we never touch the 310 MB GraphML.
    Run the real disk version with:  pytest --slow
    """

    def setUp(self):
        self.synthetic_graph = _build_synthetic_graph()

    @patch("src.utils.lookup.load_graph")
    def test_coords_to_street_returns_string(self, mock_load):
        mock_load.return_value = self.synthetic_graph
        street = coords_to_street(30.0405, 31.2305)
        self.assertIsInstance(street, str)
        self.assertTrue(len(street) > 0)

    @patch("src.utils.lookup.load_graph")
    def test_coords_to_street_known_location(self, mock_load):
        mock_load.return_value = self.synthetic_graph
        street = coords_to_street(30.0405, 31.2305)
        self.assertEqual(street, "Tahrir Street")

    def test_invalid_coordinates_raise(self):
        with self.assertRaises(ValueError):
            coords_to_street(100, 31.23)


@pytest.mark.slow
class TestCoordsToStreetIntegration(unittest.TestCase):
    """Real disk load – skipped by default. Run with: pytest --slow"""

    def test_coords_to_street_real(self):
        street = coords_to_street(30.0444, 31.2357)
        self.assertIsInstance(street, str)
        self.assertTrue(len(street) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)