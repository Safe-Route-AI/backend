def get_segment_centroid(segment_nodes: list) -> tuple:
    """
    Calculates the center point of a street segment given its nodes.
    """
    if not segment_nodes:
        return 0.0, 0.0
        
    avg_lat = sum(node['lat'] for node in segment_nodes) / len(segment_nodes)
    avg_lon = sum(node['lon'] for node in segment_nodes) / len(segment_nodes)
    
    return avg_lat, avg_lon


"""
src/utils/geometry.py
Segment Centroid Computation (Design Doc 4.9)
"""

from shapely.geometry import LineString


def get_segment_centroid(graph, u, v):
    """
    Return the (lat, lon) centroid of the edge connecting nodes u and v.

    Uses the edge's 'geometry' attribute (a Shapely LineString) when
    available, otherwise falls back to the midpoint of the two
    endpoint node coordinates.
    """
    edge_data = graph.get_edge_data(u, v)
    if edge_data is None:
        raise ValueError(f"No edge found between nodes {u} and {v}")

    # OSMnx graphs are MultiDiGraphs -> edge_data is {key: attrs, ...}
    first_edge = edge_data[0] if 0 in edge_data else next(iter(edge_data.values()))
    geometry = first_edge.get("geometry")

    if isinstance(geometry, LineString):
        centroid = geometry.centroid
        return (centroid.y, centroid.x)  # (lat, lon)

    # Fallback: average the two endpoint nodes
    u_node = graph.nodes[u]
    v_node = graph.nodes[v]
    lat = (u_node["y"] + v_node["y"]) / 2
    lon = (u_node["x"] + v_node["x"]) / 2
    return (lat, lon)