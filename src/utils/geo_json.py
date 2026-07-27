from __future__ import annotations

import networkx as nx


def paths_to_geojson(
    graph: nx.MultiDiGraph,
    paths: list[list[int]],
) -> dict:
    """
    Convert a list of node-id paths into a GeoJSON FeatureCollection.

    Each path is converted into a GeoJSON LineString Feature using the
    latitude/longitude coordinates stored in the graph nodes.

    Args:
        graph: OSMnx road network graph.
        paths: List of paths, where each path is a list of node IDs.

    Returns:
        A GeoJSON FeatureCollection dictionary.
    """

    features = []

    for path in paths:
        coordinates = []

        for node in path:
            node_data = graph.nodes[node]

            coordinates.append([
                node_data["x"],  # longitude
                node_data["y"],  # latitude
            ])

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates,
            },
            "properties": {},
        }

        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
    }