"""2D map projection visualization of satellites."""

import plotly.graph_objects as go
from typing import List, Optional
import numpy as np

from ..models import OrbitalObject


class Map2DVisualization:
    """Create 2D map visualizations of satellite positions."""
    
    def create_visualization(
        self,
        satellites: List[OrbitalObject],
        title: str = "Satellites on World Map",
        projection: str = 'natural earth',
        max_satellites: Optional[int] = None,
        color_by: str = 'altitude'
    ) -> go.Figure:
        """
        Create a 2D map visualization of satellites.
        
        Args:
            satellites: List of OrbitalObject instances to visualize
            title: Title for the visualization
            projection: Map projection type ('natural earth', 'orthographic', 'mercator')
            max_satellites: Maximum number of satellites to display
            color_by: What to color satellites by ('altitude', 'type', 'name')
            
        Returns:
            Plotly Figure object
        """
        # Filter satellites with position data
        satellites_with_pos = [
            sat for sat in satellites
            if sat.has_position()
        ]
        
        if max_satellites:
            satellites_with_pos = satellites_with_pos[:max_satellites]
        
        if not satellites_with_pos:
            # Create empty map
            fig = go.Figure()
            fig.add_trace(go.Scattergeo())
            fig.update_layout(title=title)
            return fig
        
        # Extract data
        lats = [sat.latitude for sat in satellites_with_pos]
        lons = [sat.longitude for sat in satellites_with_pos]
        names = [sat.name for sat in satellites_with_pos]
        norad_ids = [sat.norad_id or 'N/A' for sat in satellites_with_pos]
        altitudes = [sat.altitude for sat in satellites_with_pos]
        
        # Determine color values
        if color_by == 'altitude':
            color_values = altitudes
            color_title = "Altitude (km)"
        elif color_by == 'type':
            color_values = [sat.object_type or 'unknown' for sat in satellites_with_pos]
            color_title = "Type"
        else:
            color_values = altitudes
            color_title = "Altitude (km)"
        
        # Create hover text
        hover_text = [
            f"{name}<br>NORAD: {norad_id}<br>Altitude: {alt:.1f} km"
            for name, norad_id, alt in zip(names, norad_ids, altitudes)
        ]
        
        # Create figure
        fig = go.Figure()
        
        # Add satellites
        fig.add_trace(go.Scattergeo(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=dict(
                size=8,
                color=color_values,
                colorscale='Viridis' if color_by == 'altitude' else 'Set1',
                colorbar=dict(title=color_title),
                showscale=True,
                line=dict(width=1, color='white')
            ),
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            name='Satellites'
        ))
        
        # Update layout based on projection
        geo_config = {
            'showland': True,
            'landcolor': 'rgb(243, 243, 243)',
            'showocean': True,
            'oceancolor': 'rgb(204, 204, 255)',
            'showlakes': True,
            'lakecolor': 'rgb(204, 204, 255)',
            'showcountries': True,
            'countrycolor': 'rgb(128, 128, 128)',
            'coastlinecolor': 'rgb(128, 128, 128)',
        }
        
        if projection == 'natural earth':
            geo_config['projection_type'] = 'natural earth'
        elif projection == 'orthographic':
            geo_config['projection_type'] = 'orthographic'
            geo_config['projection_rotation'] = dict(lon=0, lat=0)
        elif projection == 'mercator':
            geo_config['projection_type'] = 'mercator'
        
        fig.update_layout(
            title=title,
            geo=geo_config,
            width=1200,
            height=800
        )
        
        return fig
    
    def show(self, fig: go.Figure):
        """Display the visualization in a browser."""
        fig.show()
    
    def save_html(self, fig: go.Figure, filename: str):
        """Save the visualization as an HTML file."""
        fig.write_html(filename)
    
    def save_image(self, fig: go.Figure, filename: str, width: int = 1920, height: int = 1080):
        """
        Save the visualization as an image file.
        
        Requires kaleido package for image export.
        """
        fig.write_image(filename, width=width, height=height)

