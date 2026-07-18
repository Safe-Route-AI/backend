"""

Map and Geospatial Utilities - routing functions.

    4.1  get_k_shortest_paths(graph, origin, destination, k=3)  
    4.11 get_travel_time(graph, path_nodes)                       
"""

from __future__ import annotations

import itertools
import logging
from typing import Any

import networkx as nx

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# 4.1  K-Shortest Paths
# --------------------------------------------------------------------------
def get_k_shortest_paths(
    graph: nx.MultiDiGraph,
    origin: Any,
    destination: Any,
    k: int = 3,
    weight: str = "length",
) -> list[list[Any]]:
    """
    Compute the k shortest simple paths between two nodes in the road graph.

    Uses NetworkX's `shortest_simple_paths` generator (Yen's algorithm), which
    yields simple paths (no repeated nodes) in strictly increasing order of
    total weight.

    Args:
        graph: OSMnx/NetworkX MultiDiGraph representing the road network.
        origin: Node ID to start from.
        destination: Node ID to end at.
        k: Number of candidate routes to return. Defaults to 3.
        weight: Edge attribute to use as the path weight (default "length",
            i.e. metres, as produced by OSMnx).

    Returns:
        A list of up to k node-id sequences (each a list of node IDs),
        ordered from shortest to longest. Returns fewer than k paths if
        fewer simple paths exist between origin and destination.

    Raises:
        ValueError: if origin/destination are not nodes in the graph, or if
            k is not a positive integer.
        nx.NetworkXNoPath: if no path exists between origin and destination.
    """
    if k < 1:
        raise ValueError(f"k must be a positive integer, got {k}")
    if origin not in graph:
        raise ValueError(f"origin node {origin!r} is not in the graph")
    if destination not in graph:
        raise ValueError(f"destination node {destination!r} is not in the graph")

    # shortest_simple_paths needs unambiguous edge weights; for a MultiDiGraph
    # collapse parallel edges to the cheapest one between each node pair.
    if graph.is_multigraph():
        simple_graph = _to_min_weight_simple_graph(graph, weight)
    else:
        simple_graph = graph

    try:
        path_generator = nx.shortest_simple_paths(
            simple_graph, origin, destination, weight=weight
        )
        k_paths = list(itertools.islice(path_generator, k))
    except nx.NetworkXNoPath:
        logger.warning("No path found between %s and %s", origin, destination)
        raise

    if len(k_paths) < k:
        logger.info(
            "Only %d of %d requested simple paths exist between %s and %s",
            len(k_paths), k, origin, destination,
        )

    return k_paths


def _to_min_weight_simple_graph(graph: nx.MultiDiGraph, weight: str) -> nx.DiGraph:
    """Collapse a MultiDiGraph's parallel edges to the cheapest edge per pair."""
    simple = nx.DiGraph()
    simple.add_nodes_from(graph.nodes(data=True))
    for u, v, data in graph.edges(data=True):
        w = data.get(weight, 1)
        if simple.has_edge(u, v):
            if w < simple[u][v].get(weight, float("inf")):
                simple[u][v].update(data)
        else:
            simple.add_edge(u, v, **data)
    return simple


