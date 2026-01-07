"""Data model for orbital objects (satellites, asteroids, etc.)."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class OrbitalObject:
    """Represents an orbital object with its position and metadata."""
    
    # Identification
    name: str
    norad_id: Optional[str] = None
    object_id: Optional[str] = None
    
    # Position (can be in various coordinate systems)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None  # in kilometers
    
    # Velocity
    velocity_x: Optional[float] = None  # km/s
    velocity_y: Optional[float] = None
    velocity_z: Optional[float] = None
    
    # Orbital elements (if available)
    inclination: Optional[float] = None  # degrees
    eccentricity: Optional[float] = None
    semi_major_axis: Optional[float] = None  # km
    argument_of_perigee: Optional[float] = None  # degrees
    right_ascension: Optional[float] = None  # degrees
    mean_anomaly: Optional[float] = None  # degrees
    
    # Metadata
    object_type: Optional[str] = None  # 'satellite', 'asteroid', 'debris', etc.
    epoch: Optional[datetime] = None  # Time of the observation/data
    
    # Raw data from API (for debugging/extended info)
    raw_data: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        """String representation of the orbital object."""
        return f"{self.name} ({self.object_type or 'unknown'})"
    
    def has_position(self) -> bool:
        """Check if the object has position data."""
        return (
            self.latitude is not None and
            self.longitude is not None and
            self.altitude is not None
        )
    
    def has_velocity(self) -> bool:
        """Check if the object has velocity data."""
        return (
            self.velocity_x is not None and
            self.velocity_y is not None and
            self.velocity_z is not None
        )

