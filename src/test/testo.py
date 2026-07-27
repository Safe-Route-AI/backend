from src.utils.caching import load_graph
from src.utils.geometry import get_segment_centroid
from src.utils.routing import get_travel_time, path_to_segments

graph = load_graph("Cairo, Egypt")

# Pick a real edge that exists in the graph to demo with
u, v, _ = next(iter(graph.edges(data=True)))  # grab the first edge
path = [u, v]

print("Travel time (min):", get_travel_time(graph, path))
print("Segments:", path_to_segments(graph, path))
print("Centroid:", get_segment_centroid(graph, u, v))