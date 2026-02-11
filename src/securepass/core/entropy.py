"""
Password Entropy Calculator Module

Calculates Shannon entropy for passwords and estimates crack time
under various attack scenarios.
"""

import math
from typing import Tuple, Dict
import string


def get_character_pool_size(password: str) -> int:
    """
    Detect the character pool size used in a password.

    Determines which character sets are present in the password:
    - Lowercase letters: 26 characters
    - Uppercase letters: 26 characters
    - Digits: 10 characters
    - Symbols: 32 characters (standard ASCII punctuation)

    Args:
        password: The password to analyze

    Returns:
        Total size of the character pool (sum of active character sets)

    Examples:
        >>> get_character_pool_size("password")
        26  # Only lowercase
        >>> get_character_pool_size("Password123!")
        94  # All character types
    """
    if not password:
        return 0

    pool_size = 0

    # Check for lowercase letters
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26

    # Check for uppercase letters
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26

    # Check for digits
    if any(c in string.digits for c in password):
        pool_size += 10

    # Check for symbols (punctuation and special characters)
    if any(c in string.punctuation for c in password):
        pool_size += 32

    return pool_size


def calculate_entropy(password: str) -> Tuple[float, int]:
    """
    Calculate Shannon entropy for a password.

    Uses the formula: entropy = log2(pool_size) × length

    Higher entropy indicates more randomness and resistance to
    brute-force attacks.

    Args:
        password: The password to analyze

    Returns:
        Tuple of (entropy_bits, character_pool_size)
        - entropy_bits: Password entropy in bits
        - character_pool_size: Size of the detected character pool

    Examples:
        >>> calculate_entropy("password")
        (37.6, 26)
        >>> calculate_entropy("P@ssw0rd!")
        (52.4, 94)
    """
    if not password:
        return (0.0, 0)

    pool_size = get_character_pool_size(password)

    if pool_size == 0:
        return (0.0, 0)

    # Shannon entropy formula
    entropy_bits = math.log2(pool_size) * len(password)

    return (entropy_bits, pool_size)


def estimate_crack_time(entropy_bits: float) -> Dict[str, str]:
    """
    Estimate time required to crack a password under different attack scenarios.

    Scenarios:
    - Online attack: 100 guesses per second (throttled web service)
    - Offline attack: 10 billion guesses per second (GPU cluster)

    Args:
        entropy_bits: Password entropy in bits

    Returns:
        Dictionary with formatted crack time estimates:
        {
            'online_attack_100_per_second': 'X years',
            'offline_attack_10B_per_second': 'X seconds'
        }

    Examples:
        >>> estimate_crack_time(40.0)
        {
            'online_attack_100_per_second': '348 centuries',
            'offline_attack_10B_per_second': '1.1 seconds'
        }
    """
    if entropy_bits <= 0:
        return {
            "online_attack_100_per_second": "instant",
            "offline_attack_10B_per_second": "instant",
        }

    # Calculate total possible combinations
    combinations = 2**entropy_bits

    # Online attack: 100 guesses/second
    online_seconds = combinations / 100
    online_time = _format_time(online_seconds)

    # Offline attack: 10 billion guesses/second
    offline_seconds = combinations / 10_000_000_000
    offline_time = _format_time(offline_seconds)

    return {
        "online_attack_100_per_second": online_time,
        "offline_attack_10B_per_second": offline_time,
    }


def _format_time(seconds: float) -> str:
    """
    Format time duration into human-readable string.

    Args:
        seconds: Time duration in seconds

    Returns:
        Formatted string (e.g., "3.2 years", "5 centuries", "instant")
    """
    if seconds < 0.001:
        return "instant"
    elif seconds < 1:
        return f"{seconds:.3f} seconds"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
    elif seconds < 604800:
        days = seconds / 86400
        return f"{days:.1f} days"
    elif seconds < 2592000:
        weeks = seconds / 604800
        return f"{weeks:.1f} weeks"
    elif seconds < 31536000:
        months = seconds / 2592000
        return f"{months:.1f} months"
    elif seconds < 3153600000:  # 100 years
        years = seconds / 31536000
        return f"{years:.1f} years"
    elif seconds < 31536000000:  # 1000 years
        centuries = seconds / 3153600000
        return f"{centuries:.1f} centuries"
    else:
        millennia = seconds / 31536000000
        return f"{millennia:.1f} millennia"
