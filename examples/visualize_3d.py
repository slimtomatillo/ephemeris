#!/usr/bin/env python3
"""Example: Create a 3D visualization of satellites around Earth."""

import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import SatelliteService
from src.visualization import Earth3DVisualization

def main():
    """Create and display a 3D visualization."""
    max_satellites = 50
    
    if len(sys.argv) > 1:
        try:
            max_satellites = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}. Using default: {max_satellites}")
    
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
        return 1
    
    print(f"\nCreating 3D visualization (showing up to {max_satellites} satellites)...")
    
    viz = Earth3DVisualization()
    fig = viz.create_visualization(
        satellites_with_pos,
        title=f"Satellites in 3D Space ({len(satellites_with_pos[:max_satellites])} shown)",
        max_satellites=max_satellites
    )
    
    # Save as HTML
    output_file = "satellites_3d.html"
    print(f"Saving to {output_file}...")
    viz.save_html(fig, output_file)
    
    print(f"\nVisualization saved to {output_file}")
    print("Opening in browser...")
    viz.show(fig)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

