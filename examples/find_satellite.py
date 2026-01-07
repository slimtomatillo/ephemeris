#!/usr/bin/env python3
"""Example: Find satellites by name."""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import SatelliteService

def main():
    """Find satellites by name."""
    if len(sys.argv) < 2:
        print("Usage: python examples/find_satellite.py <satellite_name>")
        print("Example: python examples/find_satellite.py ISS")
        return 1
    
    search_name = sys.argv[1]
    
    print(f"Searching for satellites matching '{search_name}'...")
    print("=" * 60)
    
    service = SatelliteService()
    
    satellites = service.find_satellite_by_name(search_name, max_results=10)
    
    if satellites:
        print(f"Found {len(satellites)} matching satellite(s):\n")
        for i, sat in enumerate(satellites, 1):
            print(f"{i}. {sat.name}")
            print(f"   NORAD ID: {sat.norad_id}")
            print(f"   Type: {sat.object_type}")
            if sat.epoch:
                print(f"   Launch Date: {sat.epoch.strftime('%Y-%m-%d')}")
            print()
    else:
        print(f"No satellites found matching '{search_name}'")
    
    print(f"Cache stats: {service.get_cache_stats()}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

