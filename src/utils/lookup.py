"""

Map and Geospatial Utilities - name/POI lookup functions.

    4.2  get_street_name(edge_data)             <- implemented here
    4.3  location_to_street(graph, lat, lon)    <- implemented here
    4.6  get_pois(lat, lon, radius_m)           <- belongs in this file
"""

from __future__ import annotations

import logging

import networkx as nx
import osmnx as ox

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# 4.2  Street Name Retrieval
# --------------------------------------------------------------------------
def get_street_name(edge_data: dict) -> str:
    """
    Extract the human-readable name of a road segment from OSMnx edge data.

    Args:
        edge_data: The edge attribute dictionary as stored by OSMnx (e.g.
            graph[u][v][0], or the third element of a (u, v, data) tuple).

    Returns:
        The street name if present ('name' key). If absent, falls back to
        the OSM 'ref' tag (road number). If neither is present, returns
        'Unnamed Road'.

        OSM data occasionally stores 'name' or 'ref' as a list (when a
        segment has multiple official names/refs); in that case the first
        entry is used.
    """
    if not edge_data:
        return "Unnamed Road"

    name = edge_data.get("name")
    if name:
        return name[0] if isinstance(name, list) else name

    ref = edge_data.get("ref")
    if ref:
        return ref[0] if isinstance(ref, list) else ref

    return "Unnamed Road"


# --------------------------------------------------------------------------
# 4.3  User Location to Street Name
# --------------------------------------------------------------------------
def location_to_street(graph: nx.MultiDiGraph, lat: float, lon: float) -> str:
    """
    Convert a GPS coordinate pair to the nearest street name.

    Uses OSMnx's nearest_edges utility to find the closest edge in the
    graph to (lat, lon), then delegates to get_street_name to retrieve the
    label. This is used to resolve the user's current position into a
    routable origin for the query pipeline.

    Args:
        graph: OSMnx/NetworkX MultiDiGraph representing the road network.
            Node coordinates must be in the 'x' (lon) / 'y' (lat) attributes
            OSMnx uses by default (i.e. the graph should be in its original
            lat/lon CRS, not a projected CRS, when calling this function).
        lat: Latitude of the query point.
        lon: Longitude of the query point.

    Returns:
        The street name of the nearest road segment (see get_street_name
        for fallback behaviour).

    Raises:
        ValueError: if lat/lon are out of valid range, or the graph is empty.
    """
    _validate_lat_lon(lat, lon)
    if graph.number_of_edges() == 0:
        raise ValueError("graph has no edges to match against")

    # osmnx.distance.nearest_edges expects (X=lon, Y=lat) order.
    u, v, _key = ox.distance.nearest_edges(graph, X=lon, Y=lat)
    edge_data = graph.get_edge_data(u, v)[_key]
    return get_street_name(edge_data)


def _validate_lat_lon(lat: float, lon: float) -> None:
    if not (-90 <= lat <= 90):
        raise ValueError(f"latitude {lat} out of range [-90, 90]")
    if not (-180 <= lon <= 180):
        raise ValueError(f"longitude {lon} out of range [-180, 180]")


