"""
Breach Detection Module

Checks passwords against the Have I Been Pwned database
using k-anonymity to protect password privacy.
"""

import hashlib
import time
from typing import Tuple, List

try:
    import requests
except ImportError:
    requests = None


def _sha1_hash(password: str) -> str:
    """
    Generate SHA-1 hash of password.
    
    Args:
        password: The password to hash
        
    Returns:
        Uppercase hexadecimal SHA-1 hash
        
    Examples:
        >>> _sha1_hash("password")
        '5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8'
    """
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()


def _api_request(hash_prefix: str, timeout: int = 10) -> List[str]:
    """
    Make request to Have I Been Pwned API.
    
    Requests all password hashes that start with the given prefix.
    
    Args:
        hash_prefix: First 5 characters of SHA-1 hash
        timeout: Request timeout in seconds
        
    Returns:
        List of hash suffixes from API response
        
    Raises:
        requests.RequestException: On network errors
    """
    if requests is None:
        raise ImportError("requests library is required for breach checking")
    
    api_url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    
    headers = {
        'User-Agent': 'SecurePass-Toolkit-v1.0',
        'Add-Padding': 'true'  # HIBP padding feature for additional privacy
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parse response (format: SUFFIX:COUNT\n)
        suffixes = []
        for line in response.text.splitlines():
            if ':' in line:
                suffix, count = line.split(':', 1)
                suffixes.append((suffix, int(count)))
        
        return suffixes
        
    except requests.Timeout:
        raise requests.RequestException("Request timed out. Check your internet connection.")
    except requests.ConnectionError:
        raise requests.RequestException("Connection failed. Check your internet connection.")
    except requests.HTTPError as e:
        raise requests.RequestException(f"HTTP error occurred: {e}")


def check_breach(password: str, timeout: int = 10, max_retries: int = 3) -> Tuple[bool, int]:
    """
    Check if password exists in Have I Been Pwned database.
    
    Uses k-anonymity model:
    1. Hashes password with SHA-1
    2. Sends only first 5 characters of hash to API
    3. Receives list of matching hash suffixes
    4. Checks locally if full hash matches
    
    This ensures the actual password is never sent to the API.
    
    Args:
        password: The password to check
        timeout: Request timeout in seconds (default: 10)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        Tuple of (is_breached, occurrence_count)
        - is_breached: True if password found in breaches
        - occurrence_count: Number of times password appeared in breaches
        
    Examples:
        >>> check_breach("password")
        (True, 9545824)  # Very common password
        >>> check_breach("xK9#mQ2$pL5@nW8")
        (False, 0)  # Strong unique password
        
    Notes:
        If network request fails after retries, returns (False, 0)
        with a warning that breach check could not be completed.
    """
    if not password:
        return (False, 0)
    
    # Step 1: Hash the password
    full_hash = _sha1_hash(password)
    hash_prefix = full_hash[:5]
    hash_suffix = full_hash[5:]
    
    # Step 2: Make API request with retry logic
    for attempt in range(max_retries):
        try:
            suffixes = _api_request(hash_prefix, timeout)
            
            # Step 3: Check if our hash suffix matches any returned suffix
            for returned_suffix, count in suffixes:
                if returned_suffix == hash_suffix:
                    return (True, count)
            
            # Not found in breach database
            return (False, 0)
            
        except Exception as e:
            if attempt < max_retries - 1:
                # Exponential backoff: wait 1s, 2s, 4s...
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                # All retries failed
                # Return False with warning rather than crashing
                # This allows offline operation
                print(f"Warning: Breach check failed after {max_retries} attempts: {e}")
                print("Password analysis will continue without breach information.")
                return (False, 0)
