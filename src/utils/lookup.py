from __future__ import annotations
"""

Map and Geospatial Utilities - name/POI lookup functions.

    4.2  get_street_name(edge_data)             <- implemented here
    4.3  location_to_street(graph, lat, lon)    <- implemented here
    4.6  get_pois(lat, lon, radius_m)           <- implemented here
    4.7 coords_to_street(lat, lon)              <- implemented here
"""

import logging

import networkx as nx
# pyrefly: ignore [missing-import]
import osmnx as ox
from src.utils.caching import load_graph

logger = logging.getLogger(__name__)

DEFAULT_PLACE = "Cairo, Egypt"


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

# --------------------------------------------------------------------------
# 4.6 Points of Interest Lookup
# --------------------------------------------------------------------------
def get_pois(
    lat: float,
    lon: float,
    radius_m: int = 300,
) -> dict[str, int]:
    """
    Retrieve nearby points of interest around a coordinate.

    Searches OpenStreetMap for nearby points of interest within the given
    radius and returns the number of police stations, hospitals,
    restaurants, metro stations, and pharmacies.

    Args:
        lat: Latitude of the query point.
        lon: Longitude of the query point.
        radius_m: Search radius in metres (default 300 m).

    Returns:
        A dictionary containing POI counts grouped by category.

    Raises:
        ValueError: If the coordinates are invalid.
    """
    _validate_lat_lon(lat, lon)

    tags = {
        "amenity": [
            "police",
            "hospital",
            "restaurant",
            "pharmacy",
        ],
        "railway": ["station"],
    }

    pois = ox.features.features_from_point(
        (lat, lon),
        tags=tags,
        dist=radius_m,
    )

    counts = {
        "police": 0,
        "hospital": 0,
        "restaurant": 0,
        "metro": 0,
        "pharmacy": 0,
    }

    if pois.empty:
        return counts

    if "amenity" in pois.columns:
        counts["police"] = (pois["amenity"] == "police").sum()
        counts["hospital"] = (pois["amenity"] == "hospital").sum()
        counts["restaurant"] = (pois["amenity"] == "restaurant").sum()
        counts["pharmacy"] = (pois["amenity"] == "pharmacy").sum()

    if "railway" in pois.columns:
        counts["metro"] = (pois["railway"] == "station").sum()

    return counts
    
# --------------------------------------------------------------------------
# 4.7   Coordinate-to-Street-Name Mapping
# --------------------------------------------------------------------------

def coords_to_street(lat: float, lon: float) -> str:
    """
    Map an arbitrary coordinate pair to the nearest street name.

    This is a convenience wrapper around location_to_street(). It loads
    the cached road graph and returns the human-readable name of the
    nearest road segment to the given coordinates.

    Args:
        lat: Latitude of the query point.
        lon: Longitude of the query point.

    Returns:
        The name of the nearest street.

    Raises:
        ValueError: If the coordinates are invalid.
    """
    _validate_lat_lon(lat, lon)
    graph = load_graph(DEFAULT_PLACE)
    return location_to_street(graph, lat, lon)

