"""3D Earth visualization with satellite positions."""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional, Dict, Any
import numpy as np

from ..models import OrbitalObject
from ..utils import lat_lon_alt_to_ecef, EARTH_RADIUS_KM


class Earth3DVisualization:
    """Create 3D visualizations of Earth with satellite positions."""
    
    def __init__(self, earth_radius_km: float = EARTH_RADIUS_KM):
        """
        Initialize the 3D Earth visualization.
        
        Args:
            earth_radius_km: Earth radius in kilometers for scaling
        """
        self.earth_radius = earth_radius_km
    
    def create_earth_sphere(self, n_points: int = 50) -> tuple:
        """
        Create a 3D sphere representing Earth.
        
        Args:
            n_points: Number of points for sphere resolution
            
        Returns:
            Tuple of (x, y, z) arrays for sphere coordinates
        """
        u = np.linspace(0, 2 * np.pi, n_points)
        v = np.linspace(0, np.pi, n_points)
        
        x = self.earth_radius * np.outer(np.cos(u), np.sin(v))
        y = self.earth_radius * np.outer(np.sin(u), np.sin(v))
        z = self.earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        return x, y, z
    
    def create_visualization(
        self,
        satellites: List[OrbitalObject],
        title: str = "Satellites in 3D Space",
        show_earth: bool = True,
        show_orbits: bool = False,
        max_satellites: Optional[int] = None
    ) -> go.Figure:
        """
        Create a 3D visualization of satellites around Earth.
        
        Args:
            satellites: List of OrbitalObject instances to visualize
            title: Title for the visualization
            show_earth: Whether to show Earth as a sphere
            show_orbits: Whether to show orbit paths (requires orbit data)
            max_satellites: Maximum number of satellites to display (None for all)
            
        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        
        # Filter satellites with position data
        satellites_with_pos = [
            sat for sat in satellites
            if sat.has_position()
        ]
        
        if max_satellites:
            satellites_with_pos = satellites_with_pos[:max_satellites]
        
        # Create Earth sphere
        if show_earth:
            x_sphere, y_sphere, z_sphere = self.create_earth_sphere()
            
            fig.add_trace(go.Surface(
                x=x_sphere,
                y=y_sphere,
                z=z_sphere,
                colorscale='Blues',
                showscale=False,
                opacity=0.6,
                name='Earth'
            ))
        
        # Add satellites
        if satellites_with_pos:
            sat_x = []
            sat_y = []
            sat_z = []
            sat_names = []
            sat_norad_ids = []
            sat_altitudes = []
            
            for sat in satellites_with_pos:
                x, y, z = lat_lon_alt_to_ecef(
                    sat.latitude,
                    sat.longitude,
                    sat.altitude
                )
                sat_x.append(x)
                sat_y.append(y)
                sat_z.append(z)
                sat_names.append(sat.name)
                sat_norad_ids.append(sat.norad_id or 'N/A')
                sat_altitudes.append(sat.altitude)
            
            # Create hover text
            hover_text = [
                f"{name}<br>NORAD: {norad_id}<br>Altitude: {alt:.1f} km"
                for name, norad_id, alt in zip(sat_names, sat_norad_ids, sat_altitudes)
            ]
            
            fig.add_trace(go.Scatter3d(
                x=sat_x,
                y=sat_y,
                z=sat_z,
                mode='markers',
                marker=dict(
                    size=5,
                    color=sat_altitudes,
                    colorscale='Viridis',
                    colorbar=dict(title="Altitude (km)"),
                    showscale=True,
                    line=dict(width=1, color='white')
                ),
                text=hover_text,
                hovertemplate='%{text}<extra></extra>',
                name='Satellites'
            ))
        
        # Update layout
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis=dict(
                    title="X (km)",
                    range=[-self.earth_radius * 2, self.earth_radius * 2]
                ),
                yaxis=dict(
                    title="Y (km)",
                    range=[-self.earth_radius * 2, self.earth_radius * 2]
                ),
                zaxis=dict(
                    title="Z (km)",
                    range=[-self.earth_radius * 2, self.earth_radius * 2]
                ),
                aspectmode='cube',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=1000,
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

