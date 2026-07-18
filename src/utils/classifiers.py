

from __future__ import annotations

import logging

import osmnx as ox

logger = logging.getLogger(__name__)

# Priority order used when multiple OSM land-use polygons overlap a point.
_AREA_TYPE_PRIORITY = ["Commercial", "Industrial", "Residential", "Mixed"]

# Maps OSM landuse / building tag values to our 4-category schema.
_LANDUSE_TO_AREA_TYPE = {
    # Commercial
    "commercial": "Commercial",
    "retail": "Commercial",
    "office": "Commercial",
    # Industrial
    "industrial": "Industrial",
    "warehouse": "Industrial",
    "port": "Industrial",
    # Residential
    "residential": "Residential",
    "apartments": "Residential",
    "house": "Residential",
    "dormitory": "Residential",
}


def _validate_lat_lon(lat: float, lon: float) -> None:
    if not (-90 <= lat <= 90):
        raise ValueError(f"latitude {lat} out of range [-90, 90]")
    if not (-180 <= lon <= 180):
        raise ValueError(f"longitude {lon} out of range [-180, 180]")


# --------------------------------------------------------------------------
# 4.4  Area Type Classification
# --------------------------------------------------------------------------
def get_area_type(lat: float, lon: float) -> str:
    """
    Classify the land-use context of a street segment centroid.

    Queries OSM land-use polygons via the Overpass API (through OSMnx's
    features_from_point) and returns the dominant land-use tag intersecting
    the coordinate, from {Residential, Commercial, Industrial, Mixed}.
    Where multiple tags overlap, the priority order
    Commercial > Industrial > Residential > Mixed is applied.

    Args:
        lat: Latitude of the segment centroid.
        lon: Longitude of the segment centroid.

    Returns:
        One of "Commercial", "Industrial", "Residential", or "Mixed".
        Returns "Mixed" if no matching land-use polygon is found, or if the
        Overpass API/network is unavailable (fail-safe neutral default).
    """
    _validate_lat_lon(lat, lon)

    tags = {"landuse": True, "building": True}
    try:
        features = ox.features_from_point((lat, lon), tags=tags, dist=50)
    except Exception as exc:  # network/Overpass failures should not crash the pipeline
        logger.warning(
            "get_area_type: could not query Overpass for (%s, %s): %s",
            lat, lon, exc,
        )
        return "Mixed"

    if features.empty:
        return "Mixed"

    found_types: set[str] = set()
    for _, row in features.iterrows():
        for column in ("landuse", "building"):
            value = row.get(column)
            if value is None or isinstance(value, float):  # NaN
                continue
            if isinstance(value, list):
                value = value[0]
            mapped = _LANDUSE_TO_AREA_TYPE.get(str(value).lower())
            if mapped:
                found_types.add(mapped)

    if not found_types:
        return "Mixed"

    for area_type in _AREA_TYPE_PRIORITY:
        if area_type in found_types:
            return area_type

    return "Mixed"