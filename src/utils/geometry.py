def get_segment_centroid(segment_nodes: list) -> tuple:
    """
    Calculates the center point of a street segment given its nodes.
    """
    if not segment_nodes:
        return 0.0, 0.0
        
    avg_lat = sum(node['lat'] for node in segment_nodes) / len(segment_nodes)
    avg_lon = sum(node['lon'] for node in segment_nodes) / len(segment_nodes)
    
    return avg_lat, avg_lon