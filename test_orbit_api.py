#!/usr/bin/env python3
"""Test the orbit API endpoint."""

import sys
import json
from src.api import UpHereClient

def main():
    """Test the orbit endpoint."""
    print("Testing UpHere Space API - Orbit Endpoint")
    print("=" * 60)
    
    client = UpHereClient()
    
    # Test ISS (NORAD ID 25544)
    satellite_id = "25544"
    print(f"\nFetching orbit data for satellite {satellite_id} (ISS)...")
    
    try:
        orbit_data = client.get_satellite_orbit(satellite_id, period=90)
        
        if orbit_data:
            print("✓ SUCCESS!")
            print(f"\nOrbit data structure:")
            print(json.dumps(orbit_data, indent=2, default=str))
            
            # Try to parse into OrbitalObject if possible
            print("\n" + "=" * 60)
            print("Attempting to parse into OrbitalObject...")
            satellite = client._parse_satellite_data(orbit_data)
            if satellite:
                print(f"Parsed satellite: {satellite.name}")
                if satellite.has_position():
                    print(f"  Position: lat={satellite.latitude}, lon={satellite.longitude}, alt={satellite.altitude} km")
        else:
            print("✗ No orbit data returned")
            print("\nNote: This might indicate:")
            print("  - API endpoint needs adjustment")
            print("  - API subscription doesn't include this endpoint")
            print("  - Check the UpHere Space API documentation")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print(f"Request stats: {client.get_request_stats()}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

