def paths_to_geojson(paths: list, graph) -> dict:
    """
    Converts graph paths to standard GeoJSON for the frontend to render.
    """
    features = []
    
    for path in paths:
        coordinates = []
        for node in path:
            # Assuming nodes have 'x' and 'y' attributes in the graph
            coordinates.append([graph.nodes[node]['x'], graph.nodes[node]['y']])
            
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {"path_length": len(path)}
        }
        features.append(feature)
        
    return {
        "type": "FeatureCollection",
        "features": features
    }