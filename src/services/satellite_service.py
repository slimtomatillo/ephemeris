"""Service layer for managing satellite data fetching and caching."""

import time
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..api import UpHereClient
from ..models import OrbitalObject


class SatelliteService:
    """Service for fetching, caching, and managing satellite data."""
    
    def __init__(self, client: Optional[UpHereClient] = None, cache_ttl_seconds: int = 300):
        """
        Initialize the satellite service.
        
        Args:
            client: UpHereClient instance (creates new one if not provided)
            cache_ttl_seconds: Time-to-live for cached data in seconds (default: 5 minutes)
        """
        self.client = client or UpHereClient()
        self.cache_ttl = cache_ttl_seconds
        
        # Cache storage
        self._satellite_list_cache: Optional[List[Dict[str, Any]]] = None
        self._satellite_list_cache_time: Optional[datetime] = None
        self._satellite_list_cache_page: Optional[int] = None
        
        self._countries_cache: Optional[List[Dict[str, Any]]] = None
        self._countries_cache_time: Optional[datetime] = None
    
    def _is_cache_valid(self, cache_time: Optional[datetime]) -> bool:
        """Check if cache is still valid."""
        if cache_time is None:
            return False
        age = datetime.now() - cache_time
        return age.total_seconds() < self.cache_ttl
    
    def get_satellites(
        self,
        page: int = 1,
        text: Optional[str] = None,
        country: Optional[str] = None,
        use_cache: bool = True
    ) -> List[OrbitalObject]:
        """
        Get list of satellites with optional caching.
        
        Args:
            page: Page number
            text: Optional text filter
            country: Optional country filter
            use_cache: Whether to use cached data if available
            
        Returns:
            List of OrbitalObject instances
        """
        # Check cache if enabled and no filters (filters make cache invalid)
        if use_cache and text is None and country is None:
            if (self._satellite_list_cache is not None and
                self._satellite_list_cache_page == page and
                self._is_cache_valid(self._satellite_list_cache_time)):
                # Return cached data
                satellites = []
                for item in self._satellite_list_cache:
                    sat = self.client._parse_satellite_data(item)
                    if sat:
                        satellites.append(sat)
                return satellites
        
        # Fetch fresh data
        satellite_list = self.client.get_satellite_list(page=page, text=text, country=country)
        
        # Cache if no filters
        if text is None and country is None:
            self._satellite_list_cache = satellite_list
            self._satellite_list_cache_time = datetime.now()
            self._satellite_list_cache_page = page
        
        # Parse into OrbitalObject instances
        satellites = []
        for item in satellite_list:
            sat = self.client._parse_satellite_data(item)
            if sat:
                satellites.append(sat)
        
        return satellites
    
    def get_countries(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get list of countries with optional caching.
        
        Args:
            use_cache: Whether to use cached data if available
            
        Returns:
            List of country dictionaries
        """
        if use_cache and self._is_cache_valid(self._countries_cache_time):
            return self._countries_cache or []
        
        countries = self.client.get_countries()
        
        if use_cache:
            self._countries_cache = countries
            self._countries_cache_time = datetime.now()
        
        return countries
    
    def find_satellite_by_name(
        self,
        name: str,
        max_results: int = 10
    ) -> List[OrbitalObject]:
        """
        Find satellites by name (case-insensitive partial match).
        
        Args:
            name: Name to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of matching OrbitalObject instances
        """
        # Use text filter for search
        satellites = self.get_satellites(text=name, use_cache=False)
        
        # Filter for case-insensitive partial match
        name_lower = name.lower()
        matches = [
            sat for sat in satellites
            if name_lower in sat.name.lower()
        ]
        
        return matches[:max_results]
    
    def find_satellite_by_norad_id(self, norad_id: str) -> Optional[OrbitalObject]:
        """
        Find a satellite by NORAD ID.
        
        Args:
            norad_id: NORAD ID to search for
            
        Returns:
            OrbitalObject instance or None if not found
        """
        # Search through cached or fresh data
        satellites = self.get_satellites(use_cache=True)
        
        for sat in satellites:
            if sat.norad_id == str(norad_id):
                return sat
        
        # If not found in first page, try searching with text filter
        # (NORAD IDs are usually numeric, so this might not work, but worth trying)
        try:
            return self.client.get_satellite_by_id(norad_id)
        except:
            pass
        
        return None
    
    def get_satellites_by_country(
        self,
        country_abbreviation: str
    ) -> List[OrbitalObject]:
        """
        Get all satellites launched by a specific country.
        
        Args:
            country_abbreviation: Country abbreviation (e.g., 'US', 'RU')
            
        Returns:
            List of OrbitalObject instances
        """
        return self.get_satellites(country=country_abbreviation, use_cache=False)
    
    def clear_cache(self):
        """Clear all cached data."""
        self._satellite_list_cache = None
        self._satellite_list_cache_time = None
        self._satellite_list_cache_page = None
        self._countries_cache = None
        self._countries_cache_time = None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about cached data."""
        stats = {
            'satellite_list_cached': self._satellite_list_cache is not None,
            'countries_cached': self._countries_cache is not None,
        }
        
        if self._satellite_list_cache_time:
            age = datetime.now() - self._satellite_list_cache_time
            stats['satellite_list_cache_age_seconds'] = age.total_seconds()
            stats['satellite_list_cache_valid'] = self._is_cache_valid(self._satellite_list_cache_time)
        
        if self._countries_cache_time:
            age = datetime.now() - self._countries_cache_time
            stats['countries_cache_age_seconds'] = age.total_seconds()
            stats['countries_cache_valid'] = self._is_cache_valid(self._countries_cache_time)
        
        return stats

