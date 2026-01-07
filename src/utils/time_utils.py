"""Time utilities for handling epochs and timestamps."""

from datetime import datetime, timezone, timedelta
from typing import Optional, Union


def parse_epoch(epoch_str: Union[str, int, float, datetime]) -> Optional[datetime]:
    """
    Parse various epoch formats into a datetime object.
    
    Args:
        epoch_str: Epoch in various formats:
                   - ISO format string: "2018-03-01T00:00:00.000Z"
                   - Unix timestamp (int or float)
                   - datetime object (returned as-is)
        
    Returns:
        datetime object or None if parsing fails
    """
    if isinstance(epoch_str, datetime):
        return epoch_str
    
    if epoch_str is None:
        return None
    
    # Try Unix timestamp
    if isinstance(epoch_str, (int, float)):
        try:
            # Check if it's in seconds (not milliseconds)
            if epoch_str > 1e10:  # Likely milliseconds
                epoch_str = epoch_str / 1000
            return datetime.fromtimestamp(epoch_str, tz=timezone.utc)
        except (ValueError, OSError):
            return None
    
    # Try ISO format
    if isinstance(epoch_str, str):
        # Remove 'Z' and replace with +00:00 for timezone
        epoch_str = epoch_str.replace('Z', '+00:00')
        
        # Try various ISO formats
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S.%f%z',
            '%Y-%m-%d %H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(epoch_str, fmt)
                # If no timezone info, assume UTC
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
    
    return None


def format_epoch(dt: datetime, format_str: str = 'iso') -> str:
    """
    Format a datetime object as an epoch string.
    
    Args:
        dt: datetime object
        format_str: Format type ('iso', 'unix', 'readable')
        
    Returns:
        Formatted string
    """
    if format_str == 'iso':
        return dt.isoformat()
    elif format_str == 'unix':
        return str(dt.timestamp())
    elif format_str == 'readable':
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    else:
        return dt.isoformat()


def time_since_epoch(epoch: datetime) -> timedelta:
    """
    Calculate time elapsed since an epoch.
    
    Args:
        epoch: datetime object
        
    Returns:
        timedelta object
    """
    now = datetime.now(timezone.utc)
    if epoch.tzinfo is None:
        epoch = epoch.replace(tzinfo=timezone.utc)
    return now - epoch


def is_recent(epoch: datetime, max_age_hours: float = 24.0) -> bool:
    """
    Check if an epoch is recent (within max_age_hours).
    
    Args:
        epoch: datetime object
        max_age_hours: Maximum age in hours
        
    Returns:
        True if epoch is within max_age_hours, False otherwise
    """
    age = time_since_epoch(epoch)
    return age.total_seconds() < (max_age_hours * 3600)

