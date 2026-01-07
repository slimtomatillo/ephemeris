# Visualization Guide

## Overview

The Ephemeris project includes two types of visualizations for displaying satellites:

1. **3D Earth Visualization** - Interactive 3D view of satellites around Earth
2. **2D Map Visualization** - Interactive 2D map projections of satellite positions

Both visualizations are built using Plotly, which provides interactive, browser-based visualizations.

## Quick Start

### 3D Visualization

```python
from src.services import SatelliteService
from src.visualization import Earth3DVisualization

# Get satellite data
service = SatelliteService()
satellites = service.get_satellites(page=1)

# Create visualization
viz = Earth3DVisualization()
fig = viz.create_visualization(satellites, max_satellites=50)

# Display
viz.show(fig)  # Opens in browser
viz.save_html(fig, "satellites_3d.html")  # Save as HTML
```

### 2D Map Visualization

```python
from src.services import SatelliteService
from src.visualization import Map2DVisualization

# Get satellite data
service = SatelliteService()
satellites = service.get_satellites(page=1)

# Create visualization
viz = Map2DVisualization()
fig = viz.create_visualization(
    satellites,
    projection='natural earth',
    max_satellites=100
)

# Display
viz.show(fig)  # Opens in browser
viz.save_html(fig, "satellites_map.html")  # Save as HTML
```

## Features

### 3D Earth Visualization

- **3D Sphere**: Earth displayed as a 3D sphere
- **Satellite Positions**: Satellites shown as colored markers
- **Color Coding**: Satellites colored by altitude
- **Interactive**: Rotate, zoom, and pan the view
- **Hover Information**: Click on satellites to see details

### 2D Map Visualization

- **Multiple Projections**: 
  - Natural Earth (default)
  - Orthographic (globe view)
  - Mercator
- **Color Coding**: Satellites colored by altitude or type
- **Interactive**: Zoom and pan the map
- **Hover Information**: Click on satellites to see details

## Position Data Requirements

**Important:** Both visualizations require satellite position data (latitude, longitude, altitude). 

- The free tier API provides satellite lists but may not include position data
- Position data is available through the `/satellites/{id}/location` endpoint
- This endpoint may require a higher subscription tier

If satellites don't have position data, the visualizations will:
- Still create the visualization structure
- Show Earth/map but no satellite markers
- Display a message indicating no position data is available

## Example Scripts

See the `examples/` directory for ready-to-use scripts:

- `examples/visualize_3d.py` - Create 3D visualization
- `examples/visualize_map.py` - Create 2D map visualization

## Customization

### Custom Colors

You can customize satellite colors by modifying the visualization code:

```python
# In earth_3d.py or map_2d.py, modify the marker color settings
marker=dict(
    size=8,
    color=custom_color_array,  # Your custom colors
    colorscale='Viridis',
    ...
)
```

### Custom Projections

For 2D maps, choose from available Plotly geo projections:
- `natural earth`
- `orthographic`
- `mercator`
- `equirectangular`
- `miller`
- And more...

## Saving Visualizations

### HTML (Interactive)

```python
viz.save_html(fig, "output.html")
```

Creates a standalone HTML file that can be opened in any browser.

### Images (Static)

```python
viz.save_image(fig, "output.png", width=1920, height=1080)
```

Requires the `kaleido` package (already included in requirements).

## Performance Considerations

- **Large Datasets**: For many satellites (>1000), consider filtering or pagination
- **3D Rendering**: 3D visualizations are more computationally intensive
- **Caching**: Use `SatelliteService` caching to avoid repeated API calls

## Future Enhancements

- Time-based animations
- Orbit path visualization
- Real-time updates
- Custom filters and search
- Multiple time points
- Trajectory prediction visualization

