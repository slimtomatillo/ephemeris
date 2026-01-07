#!/usr/bin/env python3
"""Test script for UpHere Space API client."""

import sys
from src.api import UpHereClient

def main():
    """Test the API client with basic functionality."""
    print("Testing UpHere Space API Client...")
    print("=" * 50)
    
    # Initialize client
    client = UpHereClient()
    print(f"Initialized client with host: {client.api_host}")
    print()
    
    # Test 1: Fetch a list of satellites (this endpoint works!)
    print("Test 1: Fetching list of satellites...")
    try:
        satellites = client.get_satellites(page=1)
        print(f"✓ Successfully fetched {len(satellites)} satellites")
        
        if satellites:
            print("\nFirst 3 satellites:")
            for i, sat in enumerate(satellites[:3], 1):
                print(f"  {i}. {sat.name} (NORAD: {sat.norad_id}, Type: {sat.object_type})")
                if sat.epoch:
                    print(f"     Launch Date: {sat.epoch}")
        else:
            print("No satellites returned.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 2: Get countries list
    print("Test 2: Fetching countries list...")
    try:
        countries = client.get_countries()
        print(f"✓ Successfully fetched {len(countries)} countries")
        if countries:
            print(f"  Sample countries: {', '.join([c.get('abbreviation', 'N/A') for c in countries[:5]])}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Test 3: Try to fetch orbit data (may require higher subscription tier)
    print("Test 3: Fetching orbit data for ISS (NORAD ID 25544)...")
    print("  Note: This endpoint may require a higher subscription tier")
    try:
        orbit_data = client.get_satellite_orbit("25544", period=90)
        
        if orbit_data:
            print("✓ Successfully fetched orbit data")
            print(f"  Number of orbit points: {len(orbit_data)}")
            if len(orbit_data) > 0:
                print(f"  First point: {orbit_data[0]}")
        else:
            print("  No orbit data returned (endpoint may not be available in current subscription)")
            
    except Exception as e:
        print(f"  Error: {e}")
        print("  (This is expected if the subscription doesn't include this endpoint)")
    
    print()
    
    # Test 4: Try to fetch satellite details (may require higher subscription tier)
    print("Test 4: Fetching details for ISS (NORAD ID 25544)...")
    print("  Note: This endpoint may require a higher subscription tier")
    try:
        details = client.get_satellite_details("25544")
        
        if details:
            print("✓ Successfully fetched satellite details")
            print(f"  Name: {details.get('name', 'N/A')}")
            print(f"  Type: {details.get('type', 'N/A')}")
            print(f"  Country: {details.get('country', 'N/A')}")
        else:
            print("  No details returned (endpoint may not be available in current subscription)")
            
    except Exception as e:
        print(f"  Error: {e}")
        print("  (This is expected if the subscription doesn't include this endpoint)")
    
    print()
    print("=" * 50)
    print(f"Request stats: {client.get_request_stats()}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

