#!/usr/bin/env python3
"""Example: Create a 2D map visualization of satellites."""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import SatelliteService
from src.visualization import Map2DVisualization

def main():
    """Create and display a 2D map visualization."""
    max_satellites = 100
    projection = 'natural earth'
    
    if len(sys.argv) > 1:
        try:
            max_satellites = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}. Using default: {max_satellites}")
    
    if len(sys.argv) > 2:
        projection = sys.argv[2]
        if projection not in ['natural earth', 'orthographic', 'mercator']:
            print(f"Invalid projection: {projection}. Using default: natural earth")
            projection = 'natural earth'
    
    print("Fetching satellite data...")
    print("=" * 60)
    
    service = SatelliteService()
    satellites = service.get_satellites(page=1)
    
    print(f"Found {len(satellites)} satellites")
    
    # Filter to satellites with position data
    satellites_with_pos = [s for s in satellites if s.has_position()]
    print(f"Satellites with position data: {len(satellites_with_pos)}")
    
    if not satellites_with_pos:
        print("\n⚠️  No satellites with position data available.")
        print("Note: Position data requires the /satellites/{id}/location endpoint,")
        print("      which may require a higher subscription tier.")
        print("\n💡 Tip: Run 'python examples/visualize_with_sample_data.py' to see")
        print("      a demonstration with sample position data.")
        print("\nCreating empty map (no satellites to display)...")
        satellites_with_pos = []
    
    print(f"\nCreating 2D map visualization (showing up to {max_satellites} satellites)...")
    print(f"Projection: {projection}")
    
    viz = Map2DVisualization()
    fig = viz.create_visualization(
        satellites_with_pos,
        title=f"Satellites on World Map ({len(satellites_with_pos[:max_satellites])} shown)",
        projection=projection,
        max_satellites=max_satellites
    )
    
    # Save as HTML
    output_file = f"satellites_map_{projection.replace(' ', '_')}.html"
    print(f"Saving to {output_file}...")
    viz.save_html(fig, output_file)
    
    print(f"\nVisualization saved to {output_file}")
    print("Opening in browser...")
    viz.show(fig)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

