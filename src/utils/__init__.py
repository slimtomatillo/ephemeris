"""Utility functions for coordinate conversions, time handling, and calculations."""

from .coordinates import (
    lat_lon_alt_to_ecef,
    ecef_to_lat_lon_alt,
    haversine_distance,
    euclidean_distance_3d,
    distance_between_satellites,
    elevation_angle,
    azimuth_angle,
    EARTH_RADIUS_KM,
    EARTH_RADIUS_M,
)

from .time_utils import (
    parse_epoch,
    format_epoch,
    time_since_epoch,
    is_recent,
)

__all__ = [
    'lat_lon_alt_to_ecef',
    'ecef_to_lat_lon_alt',
    'haversine_distance',
    'euclidean_distance_3d',
    'distance_between_satellites',
    'elevation_angle',
    'azimuth_angle',
    'EARTH_RADIUS_KM',
    'EARTH_RADIUS_M',
    'parse_epoch',
    'format_epoch',
    'time_since_epoch',
    'is_recent',
]

