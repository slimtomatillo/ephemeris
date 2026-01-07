"""Client for UpHere Space API."""

import os
import time
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime

from dotenv import load_dotenv
from ..models.orbital_object import OrbitalObject

# Load environment variables
load_dotenv()


class UpHereClient:
    """Client for interacting with the UpHere Space API via RapidAPI."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_host: Optional[str] = None,
        application_id: Optional[str] = None
    ):
        """
        Initialize the UpHere API client.
        
        Args:
            api_key: RapidAPI key (defaults to RAPIDAPI_KEY env var)
            api_host: RapidAPI host (defaults to RAPIDAPI_HOST env var)
            application_id: Application ID (defaults to APPLICATION_ID env var)
        """
        self.api_key = api_key or os.getenv('RAPIDAPI_KEY', '1ef82b6f37msh5032be3b5a18f87p16b060jsn2c0e142c9910')
        self.api_host = api_host or os.getenv('RAPIDAPI_HOST', 'uphere-space1.p.rapidapi.com')
        self.application_id = application_id or os.getenv('APPLICATION_ID', 'default-application_11453415')
        
        self.base_url = f"https://{self.api_host}"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': self.api_host,
            'Content-Type': 'application/json'
        }
        
        # Rate limiting tracking
        # Free tier: 1 request per second maximum
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests (1 second for free tier)
        self.request_count = 0
        self.rate_limit_retries = 3  # Number of retries on rate limit errors
    
    def set_rate_limit(self, requests_per_second: float):
        """
        Set the rate limit for API requests.
        
        Args:
            requests_per_second: Maximum number of requests per second allowed
                                (e.g., 1.0 for free tier, 10.0 for higher tiers)
        """
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be greater than 0")
        self.min_request_interval = 1.0 / requests_per_second
    
    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the API with rate limiting and error handling.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method
            params: Query parameters
            data: Request body data
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Rate limiting: ensure minimum time between requests (1 req/sec for free tier)
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Retry logic for rate limit errors
        for attempt in range(self.rate_limit_retries):
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, headers=self.headers, params=params, timeout=30)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=self.headers, json=data, params=params, timeout=30)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                self.last_request_time = time.time()
                self.request_count += 1
                
                return response.json()
                
            except requests.exceptions.Timeout:
                raise Exception(f"Request to {endpoint} timed out")
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    # Rate limit exceeded - wait and retry
                    if attempt < self.rate_limit_retries - 1:
                        # Exponential backoff: wait longer on each retry
                        wait_time = (attempt + 1) * self.min_request_interval
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(
                            f"Rate limit exceeded after {self.rate_limit_retries} retries. "
                            f"Free tier allows 1 request per second. Please wait before making more requests."
                        )
                elif response.status_code == 401:
                    raise Exception(f"Authentication failed. Check your API key.")
                elif response.status_code == 404:
                    raise Exception(
                        f"Endpoint not found (404). This may indicate:\n"
                        f"  - The endpoint path is incorrect\n"
                        f"  - Your API subscription doesn't include this endpoint\n"
                        f"  - The endpoint needs to be activated in RapidAPI dashboard\n"
                        f"  - Check the API documentation: https://uphere.space/development/api/documentation\n"
                        f"  - Check the RapidAPI playground for available endpoints"
                    )
                else:
                    raise Exception(f"HTTP error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Request failed: {str(e)}")
        
        # Should not reach here, but just in case
        raise Exception(f"Request to {endpoint} failed after {self.rate_limit_retries} attempts")
    
    def get_satellite_list(
        self,
        page: int = 1,
        text: Optional[str] = None,
        country: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get a list of satellites with details.
        
        Args:
            page: Page number (required)
            text: Optional text filter to search satellites
            country: Optional country abbreviation to filter by launch country
            
        Returns:
            List of satellite dictionaries
        """
        try:
            params = {'page': page}
            if text:
                params['text'] = text
            if country:
                params['country'] = country
            
            response = self._make_request('satellite/list', params=params)
            
            return response if isinstance(response, list) else []
            
        except Exception as e:
            print(f"Error fetching satellite list: {e}")
            return []
    
    def get_satellites(
        self,
        page: int = 1,
        text: Optional[str] = None,
        country: Optional[str] = None
    ) -> List[OrbitalObject]:
        """
        Fetch satellite data from the API and parse into OrbitalObject instances.
        
        Args:
            page: Page number (required, default: 1)
            text: Optional text filter to search satellites
            country: Optional country abbreviation to filter by launch country
            
        Returns:
            List of OrbitalObject instances
        """
        try:
            satellite_list = self.get_satellite_list(page=page, text=text, country=country)
            
            # Parse response into OrbitalObject instances
            satellites = []
            for item in satellite_list:
                satellite = self._parse_satellite_data(item)
                if satellite:
                    satellites.append(satellite)
            
            return satellites
            
        except Exception as e:
            print(f"Error fetching satellites: {e}")
            return []
    
    def get_visible_satellites(
        self,
        lat: float,
        lng: float
    ) -> List[Dict[str, Any]]:
        """
        Get a list of satellites visible from a specific location.
        
        Args:
            lat: Latitude of the observation location
            lng: Longitude of the observation location
            
        Returns:
            List of visible satellites with name, number, and coordinates
        """
        try:
            response = self._make_request(
                'user/visible',
                params={'lat': str(lat), 'lng': str(lng)}
            )
            
            return response if isinstance(response, list) else []
            
        except Exception as e:
            print(f"Error fetching visible satellites: {e}")
            return []
    
    def get_launch_sites(self) -> List[Dict[str, Any]]:
        """
        Get a list of satellite launch sites from around the world.
        
        Returns:
            List of launch site dictionaries
        """
        try:
            response = self._make_request('satellite/list/launch-sites')
            
            return response if isinstance(response, list) else []
            
        except Exception as e:
            print(f"Error fetching launch sites: {e}")
            return []
    
    def get_countries(self) -> List[Dict[str, Any]]:
        """
        Get a list of countries available to filter satellite lists.
        
        Returns:
            List of country dictionaries with id, name, and abbreviation
        """
        try:
            response = self._make_request('satellite/list/countries')
            
            return response if isinstance(response, list) else []
            
        except Exception as e:
            print(f"Error fetching countries: {e}")
            return []
    
    def get_satellite_location(
        self,
        satellite_id: str,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        units: str = 'imperial'
    ) -> Optional[Dict[str, Any]]:
        """
        Get the current location of a satellite by its NORAD ID.
        
        Args:
            satellite_id: NORAD ID (satellite number)
            lat: Optional latitude for elevation/azimuth calculation
            lng: Optional longitude for elevation/azimuth calculation
            units: Units for measurements ('metric' or 'imperial', default: 'imperial')
            
        Returns:
            Dictionary with location data or None if not found
        """
        try:
            params = {'units': units}
            if lat is not None:
                params['lat'] = lat
            if lng is not None:
                params['lng'] = lng
            
            response = self._make_request(
                f'satellites/{satellite_id}/location',
                params=params
            )
            
            return response if isinstance(response, dict) else None
            
        except Exception as e:
            print(f"Error fetching location for satellite {satellite_id}: {e}")
            return None
    
    def get_satellite_orbit(
        self,
        satellite_id: str,
        period: int = 90
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get the orbital track for a satellite using the NORAD ID.
        
        Args:
            satellite_id: NORAD ID (satellite number)
            period: Time period in minutes for orbit prediction (required, default: 90)
            
        Returns:
            List of orbit points, each containing lat, lng, and date, or None if not found
        """
        try:
            response = self._make_request(
                f'satellites/{satellite_id}/orbit',
                params={'period': period}
            )
            
            return response if isinstance(response, list) else None
            
        except Exception as e:
            print(f"Error fetching orbit data for satellite {satellite_id}: {e}")
            return None
    
    def get_satellite_details(self, satellite_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the details for a satellite using the NORAD ID.
        
        Args:
            satellite_id: NORAD ID (satellite number)
            
        Returns:
            Dictionary with satellite details or None if not found
        """
        try:
            response = self._make_request(f'satellites/{satellite_id}/details')
            
            return response if isinstance(response, dict) else None
            
        except Exception as e:
            print(f"Error fetching details for satellite {satellite_id}: {e}")
            return None
    
    def get_satellite_by_id(self, satellite_id: str) -> Optional[OrbitalObject]:
        """
        Fetch a specific satellite by ID using the details endpoint.
        
        Args:
            satellite_id: NORAD ID or other identifier
            
        Returns:
            OrbitalObject instance or None if not found
        """
        try:
            details = self.get_satellite_details(satellite_id)
            if details:
                return self._parse_satellite_data(details)
            return None
            
        except Exception as e:
            print(f"Error fetching satellite {satellite_id}: {e}")
            return None
    
    def _parse_satellite_data(self, data: Dict[str, Any]) -> Optional[OrbitalObject]:
        """
        Parse API response data into an OrbitalObject.
        
        Handles multiple API response formats:
        - Details endpoint: name, number, type, country, etc.
        - Location endpoint: coordinates, height, speed, etc.
        - List endpoint: name, number, classification, etc.
        
        Args:
            data: Raw data from API
            
        Returns:
            OrbitalObject instance or None if parsing fails
        """
        try:
            # Extract name (varies by endpoint)
            name = data.get('name', 'Unknown')
            
            # Extract NORAD ID (varies by endpoint - 'number' or 'norad_id')
            norad_id = str(data.get('number') or data.get('norad_id') or data.get('id', ''))
            
            # Position data - from location endpoint or coordinates
            latitude = None
            longitude = None
            altitude = None
            
            # Location endpoint format: coordinates array [lng, lat]
            if 'coordinates' in data and isinstance(data['coordinates'], list):
                if len(data['coordinates']) >= 2:
                    longitude = float(data['coordinates'][0])
                    latitude = float(data['coordinates'][1])
            
            # Direct latitude/longitude fields
            if 'latitude' in data:
                latitude = float(data['latitude'])
            if 'longitude' in data:
                longitude = float(data['longitude'])
            
            # Altitude/height
            altitude = data.get('altitude') or data.get('height')
            if altitude is not None:
                altitude = float(altitude)
            
            # Speed (from location endpoint)
            speed = data.get('speed')
            
            # Parse launch date if available
            epoch = None
            launch_date = data.get('launch_date')
            if launch_date:
                try:
                    # Try ISO format
                    epoch = datetime.fromisoformat(str(launch_date).replace('Z', '+00:00'))
                except:
                    pass
            
            # Orbital period (from details endpoint)
            orbital_period = data.get('orbital_period')
            
            # Object type
            object_type = data.get('type') or data.get('classification') or 'satellite'
            
            return OrbitalObject(
                name=name,
                norad_id=norad_id if norad_id else None,
                object_id=str(data.get('id', '')),
                latitude=latitude,
                longitude=longitude,
                altitude=altitude,
                velocity_x=None,  # Not provided in API responses
                velocity_y=None,
                velocity_z=None,
                inclination=None,
                eccentricity=None,
                semi_major_axis=None,
                object_type=object_type.lower() if object_type else 'satellite',
                epoch=epoch,
                raw_data=data
            )
            
        except Exception as e:
            print(f"Error parsing satellite data: {e}")
            print(f"Data: {data}")
            return None
    
    def get_request_stats(self) -> Dict[str, Any]:
        """
        Get statistics about API requests made.
        
        Returns:
            Dictionary with request statistics including rate limit info
        """
        time_since_last = time.time() - self.last_request_time if self.last_request_time > 0 else 0
        return {
            'request_count': self.request_count,
            'last_request_time': self.last_request_time,
            'time_since_last_request': time_since_last,
            'min_request_interval': self.min_request_interval,
            'rate_limit': f"{1/self.min_request_interval:.1f} requests/second",
            'can_make_request_now': time_since_last >= self.min_request_interval
        }

