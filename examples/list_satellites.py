#!/usr/bin/env python3
"""Example: List satellites with filtering options."""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import SatelliteService

def main():
    """List satellites with optional filters."""
    page = 1
    country = None
    
    # Parse arguments
    if len(sys.argv) > 1:
        try:
            page = int(sys.argv[1])
        except ValueError:
            print(f"Invalid page number: {sys.argv[1]}")
            return 1
    
    if len(sys.argv) > 2:
        country = sys.argv[2]
    
    print("Fetching satellite list...")
    if country:
        print(f"Filtering by country: {country}")
    print("=" * 60)
    
    service = SatelliteService()
    
    satellites = service.get_satellites(page=page, country=country)
    
    print(f"\nPage {page}: Found {len(satellites)} satellites\n")
    
    for i, sat in enumerate(satellites[:20], 1):  # Show first 20
        print(f"{i:3d}. {sat.name:40s} NORAD: {sat.norad_id:8s} Type: {sat.object_type or 'N/A':10s}")
    
    if len(satellites) > 20:
        print(f"\n... and {len(satellites) - 20} more")
    
    print(f"\nCache stats: {service.get_cache_stats()}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

