import os

def get_segment_image(lat: float, lon: float) -> str:
    """
    Returns a mocked local path for the street imagery based on coordinates.
    """
    # Fallback default image path in case mapping fails
    default_path = "data/street_imagery/default.jpg"
    
    # In a real scenario, this maps lat/lon to a specific file
    mapped_path = f"data/street_imagery/{round(lat, 3)}_{round(lon, 3)}.jpg"
    
    if os.path.exists(mapped_path):
        return mapped_path
    return default_path


"""
src/utils/image_mapper.py
Edge-to-Image Mapping (Design Doc 4.10)
"""

import json
import os
import numpy as np
# pyrefly: ignore [missing-import]
import cv2

_INDEX_PATH = os.path.join("data", "graph_cache", "edge_image_index.json")
_index_cache = None


def _load_index():
    global _index_cache
    if _index_cache is None:
        if os.path.exists(_INDEX_PATH):
            with open(_INDEX_PATH, "r") as f:
                _index_cache = json.load(f)
        else:
            _index_cache = {}
    return _index_cache


def get_segment_image(u, v):
    """
    Return a representative street-view image (NumPy array, BGR) for
    the segment (u, v). O(1) lookup against a pre-built offline index.
    Falls back to a neutral grey placeholder if no mapping exists.
    """
    index = _load_index()
    image_path = index.get(f"{u}_{v}")

    if image_path and os.path.exists(image_path):
        image = cv2.imread(image_path)
        if image is not None:
            return image

    # Neutral grey placeholder (mean brightness / crowd = neutral)
    return np.full((224, 224, 3), 128, dtype=np.uint8)