import unittest
import networkx as nx

from src.utils.geo_json import paths_to_geojson


class TestPathsToGeoJson(unittest.TestCase):

    def test_paths_to_geojson(self):
        graph = nx.MultiDiGraph()

        graph.add_node(1, x=31.2, y=30.1)
        graph.add_node(2, x=31.3, y=30.2)

        graph.add_edge(1, 2)

        geojson = paths_to_geojson(
            graph,
            [[1, 2]],
        )

        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertEqual(len(geojson["features"]), 1)
        self.assertEqual(
            geojson["features"][0]["geometry"]["type"],
            "LineString",
        )
        self.assertEqual(
            geojson["features"][0]["geometry"]["coordinates"],
            [
                [31.2, 30.1],
                [31.3, 30.2],
            ],
        )



if __name__ == "__main__":
    unittest.main()