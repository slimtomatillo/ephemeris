# Example Scripts

This directory contains example scripts demonstrating how to use the Ephemeris API client and utilities.

## Available Examples

### 1. `list_satellites.py` - List Satellites

List satellites with optional pagination and country filtering.

**Usage:**
```bash
# List first page
python examples/list_satellites.py

# List specific page
python examples/list_satellites.py 2

# Filter by country
python examples/list_satellites.py 1 US
```

**Example Output:**
```
Page 1: Found 50 satellites

  1. SPACE STATION                    NORAD: 25544    Type: payload
  2. HST                              NORAD: 20580    Type: payload
  3. IRIS                             NORAD: 39197    Type: payload
  ...
```

### 2. `find_satellite.py` - Find Satellite by Name

Search for satellites by name (case-insensitive partial match).

**Usage:**
```bash
python examples/find_satellite.py ISS
python examples/find_satellite.py "SPACE STATION"
python examples/find_satellite.py Hubble
```

**Example Output:**
```
Found 1 matching satellite(s):

1. SPACE STATION
   NORAD ID: 25544
   Type: payload
   Launch Date: 1998-11-20
```

### 3. `satellite_distance.py` - Calculate Distance Between Satellites

Calculate the distance between two satellites (requires position data).

**Usage:**
```bash
python examples/satellite_distance.py 25544 20580
```

**Note:** This requires satellite position data, which may not be available in the free tier. The script will show what data is available.

## Running Examples

Make sure you're in the project root directory and have activated the virtual environment:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python examples/list_satellites.py
```

## Using the Utilities

### Coordinate Conversions

```python
from src.utils import lat_lon_alt_to_ecef, distance_between_satellites

# Convert lat/lon/alt to 3D coordinates
x, y, z = lat_lon_alt_to_ecef(45.0, -122.0, 400.0)  # ISS example

# Calculate distance between two satellites
distance = distance_between_satellites(
    lat1=45.0, lon1=-122.0, alt1=400.0,
    lat2=45.5, lon2=-122.5, alt2=500.0
)
```

### Time Utilities

```python
from src.utils import parse_epoch, format_epoch
from datetime import datetime

# Parse various epoch formats
epoch = parse_epoch("2018-03-01T00:00:00.000Z")
epoch = parse_epoch(1519862400)  # Unix timestamp

# Format epoch
formatted = format_epoch(epoch, format_str='readable')
```

### Satellite Service

```python
from src.services import SatelliteService

service = SatelliteService()

# Get satellites (with caching)
satellites = service.get_satellites(page=1)

# Find by name
matches = service.find_satellite_by_name("ISS")

# Find by NORAD ID
satellite = service.find_satellite_by_norad_id("25544")

# Get by country
us_satellites = service.get_satellites_by_country("US")
```

## Rate Limiting

All examples respect the API rate limit (1 request per second for free tier). The client automatically handles spacing between requests.

