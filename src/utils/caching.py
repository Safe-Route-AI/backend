"""
Graph loading and caching utilities.
"""

from __future__ import annotations

import logging
from pathlib import Path

import networkx as nx
# pyrefly: ignore [missing-import]
import osmnx as ox

logger = logging.getLogger(__name__)

# In-memory cache
_GRAPH_CACHE: dict[str, nx.MultiDiGraph] = {}

def load_graph(place_name: str) -> nx.MultiDiGraph:
    """
    Load and cache the road network for a given place.

    If the graph already exists in memory, return it immediately.
    Otherwise, try loading it from disk. If no saved graph exists,
    download it from OpenStreetMap, save it, cache it, then return it.

    Args:
        place_name: Name of the area (e.g. "Cairo, Egypt").

    Returns:
        A NetworkX MultiDiGraph representing the road network.
    """

    # Return the graph immediately if it is already cached.
    if place_name in _GRAPH_CACHE:
        logger.info("Using cached graph for %s", place_name)
        return _GRAPH_CACHE[place_name]

    # Create a safe filename for the graph.
    filename = (
        place_name.replace(",", "")
        .replace(" ", "_")
        .replace("/", "_")
    )

    graph_dir = Path("graphs")
    graph_file = graph_dir / f"{filename}.graphml"

    # Load the graph from disk if it already exists.
    if graph_file.exists():
        logger.info("Loading graph from disk: %s", graph_file)

        graph = ox.load_graphml(graph_file)

        _GRAPH_CACHE[place_name] = graph

        return graph

    # Download the graph from OpenStreetMap.
    logger.info("Downloading graph for %s", place_name)

    graph = ox.graph_from_place(
        place_name,
        network_type="walk",
    )

    # Create the graphs directory if it does not exist.
    graph_dir.mkdir(parents=True, exist_ok=True)

    # Save the graph to disk for future use.
    ox.save_graphml(graph, graph_file)

    # Store the graph in the in-memory cache.
    _GRAPH_CACHE[place_name] = graph

    logger.info("Graph cached successfully for %s", place_name)

    return graph

    # shahd notes for load_graph function
    # network type 3mltha walk msh drive (app for walking)
    # general graphs ya3ny msh madina mo3ina
    # m3mltsh projection
