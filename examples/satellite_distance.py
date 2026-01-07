#!/usr/bin/env python3
"""Example: Calculate distance between satellites."""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import SatelliteService
from src.utils import distance_between_satellites, haversine_distance

def main():
    """Calculate distance between two satellites."""
    if len(sys.argv) < 3:
        print("Usage: python examples/satellite_distance.py <norad_id1> <norad_id2>")
        print("Example: python examples/satellite_distance.py 25544 20580")
        print("\nNote: This requires satellite position data, which may not be available")
        print("      in the free tier. The example will show what data is available.")
        return 1
    
    norad_id1 = sys.argv[1]
    norad_id2 = sys.argv[2]
    
    print(f"Finding satellites {norad_id1} and {norad_id2}...")
    print("=" * 60)
    
    service = SatelliteService()
    
    sat1 = service.find_satellite_by_norad_id(norad_id1)
    sat2 = service.find_satellite_by_norad_id(norad_id2)
    
    if not sat1:
        print(f"Satellite {norad_id1} not found")
        return 1
    
    if not sat2:
        print(f"Satellite {norad_id2} not found")
        return 1
    
    print(f"\nSatellite 1: {sat1.name} (NORAD: {sat1.norad_id})")
    print(f"Satellite 2: {sat2.name} (NORAD: {sat2.norad_id})")
    print()
    
    # Check if we have position data
    if sat1.has_position() and sat2.has_position():
        # Calculate 3D distance
        distance_3d = distance_between_satellites(
            sat1.latitude, sat1.longitude, sat1.altitude,
            sat2.latitude, sat2.longitude, sat2.altitude
        )
        
        # Calculate surface distance (great circle)
        surface_distance = haversine_distance(
            sat1.latitude, sat1.longitude,
            sat2.latitude, sat2.longitude
        )
        
        print(f"3D Distance: {distance_3d:.2f} km")
        print(f"Surface Distance: {surface_distance:.2f} km")
        print(f"Altitude Difference: {abs(sat1.altitude - sat2.altitude):.2f} km")
    else:
        print("Position data not available for one or both satellites.")
        print("This may require a higher subscription tier to access location endpoints.")
        print("\nAvailable data:")
        print(f"  {sat1.name}: position={sat1.has_position()}")
        print(f"  {sat2.name}: position={sat2.has_position()}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

