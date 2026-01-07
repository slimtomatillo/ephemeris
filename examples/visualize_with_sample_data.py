#!/usr/bin/env python3
"""Example: Create visualization with sample satellite position data."""

import sys
import os
import random
from datetime import datetime

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import OrbitalObject
from src.visualization import Earth3DVisualization, Map2DVisualization

def create_sample_satellites(count: int = 20) -> list:
    """
    Create sample satellites with realistic position data for demonstration.
    
    Args:
        count: Number of sample satellites to create
        
    Returns:
        List of OrbitalObject instances with position data
    """
    satellites = []
    
    # Some well-known satellites with approximate positions
    sample_data = [
        {"name": "ISS", "norad_id": "25544", "altitude": 408, "type": "payload"},
        {"name": "HST", "norad_id": "20580", "altitude": 540, "type": "payload"},
        {"name": "AQUA", "norad_id": "27424", "altitude": 705, "type": "payload"},
        {"name": "GOES 17", "norad_id": "43226", "altitude": 35786, "type": "payload"},
        {"name": "GPS IIF-12", "norad_id": "41019", "altitude": 20200, "type": "payload"},
    ]
    
    # Add known satellites
    for data in sample_data[:min(count, len(sample_data))]:
        # Generate random position (for demo purposes)
        lat = random.uniform(-60, 60)
        lon = random.uniform(-180, 180)
        
        sat = OrbitalObject(
            name=data["name"],
            norad_id=data["norad_id"],
            latitude=lat,
            longitude=lon,
            altitude=data["altitude"],
            object_type=data["type"],
            epoch=datetime.now()
        )
        satellites.append(sat)
    
    # Add more random satellites to reach count
    for i in range(len(satellites), count):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        altitude = random.choice([
            random.uniform(200, 600),      # LEO
            random.uniform(600, 2000),    # MEO
            random.uniform(20000, 36000), # GEO
        ])
        
        sat = OrbitalObject(
            name=f"Satellite {i+1}",
            norad_id=str(10000 + i),
            latitude=lat,
            longitude=lon,
            altitude=altitude,
            object_type="payload",
            epoch=datetime.now()
        )
        satellites.append(sat)
    
    return satellites

def main():
    """Create visualizations with sample data."""
    count = 20
    
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}. Using default: {count}")
    
    viz_type = 'both'
    if len(sys.argv) > 2:
        viz_type = sys.argv[2].lower()
        if viz_type not in ['3d', '2d', 'both']:
            viz_type = 'both'
    
    print("Creating sample satellite data for demonstration...")
    print("=" * 60)
    
    satellites = create_sample_satellites(count)
    
    print(f"Created {len(satellites)} sample satellites with position data")
    print("\nSample satellites:")
    for sat in satellites[:5]:
        print(f"  {sat.name}: lat={sat.latitude:.2f}°, lon={sat.longitude:.2f}°, alt={sat.altitude:.1f} km")
    
    # Create 3D visualization
    if viz_type in ['3d', 'both']:
        print("\n" + "=" * 60)
        print("Creating 3D visualization...")
        viz_3d = Earth3DVisualization()
        fig_3d = viz_3d.create_visualization(
            satellites,
            title=f"Sample Satellites in 3D Space ({len(satellites)} satellites)",
            max_satellites=count
        )
        
        output_3d = "sample_satellites_3d.html"
        viz_3d.save_html(fig_3d, output_3d)
        print(f"Saved to {output_3d}")
        print("Opening in browser...")
        viz_3d.show(fig_3d)
    
    # Create 2D map visualization
    if viz_type in ['2d', 'both']:
        print("\n" + "=" * 60)
        print("Creating 2D map visualization...")
        viz_2d = Map2DVisualization()
        fig_2d = viz_2d.create_visualization(
            satellites,
            title=f"Sample Satellites on World Map ({len(satellites)} satellites)",
            projection='natural earth',
            max_satellites=count
        )
        
        output_2d = "sample_satellites_map.html"
        viz_2d.save_html(fig_2d, output_2d)
        print(f"Saved to {output_2d}")
        print("Opening in browser...")
        viz_2d.show(fig_2d)
    
    print("\n" + "=" * 60)
    print("Note: These are sample positions for demonstration.")
    print("Real position data requires a higher API subscription tier.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

