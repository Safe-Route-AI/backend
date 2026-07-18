"""Tests for src.utils.classifiers.get_area_type (4.4)."""

import unittest
from unittest.mock import patch

import geopandas as gpd
from shapely.geometry import Point

from src.utils.classifiers import get_area_type


def _fake_features(rows):
    return gpd.GeoDataFrame(rows, geometry=[Point(0, 0)] * len(rows) if rows else [])


class TestGetAreaType(unittest.TestCase):
    @patch("src.utils.classifiers.ox.features_from_point")
    def test_commercial_wins_priority(self, mock_features):
        mock_features.return_value = _fake_features(
            [{"landuse": "residential"}, {"landuse": "commercial"}]
        )
        self.assertEqual(get_area_type(30.04, 31.23), "Commercial")

    @patch("src.utils.classifiers.ox.features_from_point")
    def test_residential_only(self, mock_features):
        mock_features.return_value = _fake_features([{"landuse": "residential"}])
        self.assertEqual(get_area_type(30.04, 31.23), "Residential")

    @patch("src.utils.classifiers.ox.features_from_point")
    def test_no_tags_found_defaults_to_mixed(self, mock_features):
        mock_features.return_value = _fake_features([])
        self.assertEqual(get_area_type(30.04, 31.23), "Mixed")

    @patch("src.utils.classifiers.ox.features_from_point")
    def test_network_error_defaults_to_mixed(self, mock_features):
        mock_features.side_effect = RuntimeError("Overpass unreachable")
        self.assertEqual(get_area_type(30.04, 31.23), "Mixed")

    def test_invalid_coordinates_raise(self):
        with self.assertRaises(ValueError):
            get_area_type(999, 31.23)


if __name__ == "__main__":
    unittest.main(verbosity=2)