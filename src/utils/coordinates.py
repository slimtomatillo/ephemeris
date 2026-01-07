"""Coordinate conversion utilities for orbital objects."""

import math
from typing import Tuple, Optional


# Earth constants
EARTH_RADIUS_KM = 6371.0  # Mean Earth radius in kilometers
EARTH_RADIUS_M = 6371000.0  # Mean Earth radius in meters


def lat_lon_alt_to_ecef(
    latitude: float,
    longitude: float,
    altitude_km: float
) -> Tuple[float, float, float]:
    """
    Convert latitude, longitude, and altitude to Earth-Centered, Earth-Fixed (ECEF) coordinates.
    
    ECEF is a Cartesian coordinate system where:
    - X: Points from Earth center through equator at 0° longitude
    - Y: Points from Earth center through equator at 90° east longitude
    - Z: Points from Earth center through North Pole
    
    Args:
        latitude: Latitude in degrees (-90 to 90)
        longitude: Longitude in degrees (-180 to 180)
        altitude_km: Altitude above sea level in kilometers
        
    Returns:
        Tuple of (x, y, z) coordinates in kilometers
    """
    # Convert to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)
    
    # Calculate distance from Earth center
    r = EARTH_RADIUS_KM + altitude_km
    
    # Calculate ECEF coordinates
    x = r * math.cos(lat_rad) * math.cos(lon_rad)
    y = r * math.cos(lat_rad) * math.sin(lon_rad)
    z = r * math.sin(lat_rad)
    
    return (x, y, z)


def ecef_to_lat_lon_alt(
    x: float,
    y: float,
    z: float
) -> Tuple[float, float, float]:
    """
    Convert ECEF coordinates to latitude, longitude, and altitude.
    
    Args:
        x: ECEF X coordinate in kilometers
        y: ECEF Y coordinate in kilometers
        z: ECEF Z coordinate in kilometers
        
    Returns:
        Tuple of (latitude, longitude, altitude_km)
    """
    # Calculate distance from Earth center
    r = math.sqrt(x*x + y*y + z*z)
    
    # Calculate latitude (in radians, then convert to degrees)
    lat_rad = math.asin(z / r)
    latitude = math.degrees(lat_rad)
    
    # Calculate longitude (in radians, then convert to degrees)
    lon_rad = math.atan2(y, x)
    longitude = math.degrees(lon_rad)
    
    # Calculate altitude
    altitude_km = r - EARTH_RADIUS_KM
    
    return (latitude, longitude, altitude_km)


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate the great-circle distance between two points on Earth using the Haversine formula.
    
    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees
        
    Returns:
        Distance in kilometers
    """
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    distance_km = EARTH_RADIUS_KM * c
    
    return distance_km


def euclidean_distance_3d(
    x1: float, y1: float, z1: float,
    x2: float, y2: float, z2: float
) -> float:
    """
    Calculate Euclidean distance between two 3D points.
    
    Args:
        x1, y1, z1: Coordinates of first point
        x2, y2, z2: Coordinates of second point
        
    Returns:
        Distance in same units as input coordinates
    """
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def distance_between_satellites(
    lat1: float, lon1: float, alt1: float,
    lat2: float, lon2: float, alt2: float
) -> float:
    """
    Calculate 3D distance between two satellites given their positions.
    
    Args:
        lat1, lon1, alt1: Position of first satellite (degrees, degrees, km)
        lat2, lon2, alt2: Position of second satellite (degrees, degrees, km)
        
    Returns:
        Distance in kilometers
    """
    # Convert both to ECEF
    x1, y1, z1 = lat_lon_alt_to_ecef(lat1, lon1, alt1)
    x2, y2, z2 = lat_lon_alt_to_ecef(lat2, lon2, alt2)
    
    # Calculate 3D distance
    return euclidean_distance_3d(x1, y1, z1, x2, y2, z2)


def elevation_angle(
    observer_lat: float,
    observer_lon: float,
    observer_alt_km: float,
    satellite_lat: float,
    satellite_lon: float,
    satellite_alt_km: float
) -> float:
    """
    Calculate the elevation angle of a satellite as seen from an observer location.
    
    Elevation angle: 0° = horizon, 90° = directly overhead
    
    Args:
        observer_lat, observer_lon, observer_alt_km: Observer position
        satellite_lat, satellite_lon, satellite_alt_km: Satellite position
        
    Returns:
        Elevation angle in degrees (0-90)
    """
    # Convert to ECEF
    obs_x, obs_y, obs_z = lat_lon_alt_to_ecef(observer_lat, observer_lon, observer_alt_km)
    sat_x, sat_y, sat_z = lat_lon_alt_to_ecef(satellite_lat, satellite_lon, satellite_alt_km)
    
    # Vector from observer to satellite
    dx = sat_x - obs_x
    dy = sat_y - obs_y
    dz = sat_z - obs_z
    
    # Horizontal distance
    horizontal_dist = math.sqrt(dx*dx + dy*dy)
    
    # Elevation angle
    elevation_rad = math.atan2(dz, horizontal_dist)
    elevation_deg = math.degrees(elevation_rad)
    
    return elevation_deg


def azimuth_angle(
    observer_lat: float,
    observer_lon: float,
    satellite_lat: float,
    satellite_lon: float
) -> float:
    """
    Calculate the azimuth angle of a satellite as seen from an observer location.
    
    Azimuth angle: 0° = North, 90° = East, 180° = South, 270° = West
    
    Args:
        observer_lat, observer_lon: Observer position
        satellite_lat, satellite_lon: Satellite position
        
    Returns:
        Azimuth angle in degrees (0-360)
    """
    # Convert to radians
    obs_lat_rad = math.radians(observer_lat)
    obs_lon_rad = math.radians(observer_lon)
    sat_lat_rad = math.radians(satellite_lat)
    sat_lon_rad = math.radians(satellite_lon)
    
    # Calculate bearing using formula
    dlon = sat_lon_rad - obs_lon_rad
    
    y = math.sin(dlon) * math.cos(sat_lat_rad)
    x = (math.cos(obs_lat_rad) * math.sin(sat_lat_rad) -
         math.sin(obs_lat_rad) * math.cos(sat_lat_rad) * math.cos(dlon))
    
    azimuth_rad = math.atan2(y, x)
    azimuth_deg = math.degrees(azimuth_rad)
    
    # Normalize to 0-360
    if azimuth_deg < 0:
        azimuth_deg += 360
    
    return azimuth_deg

