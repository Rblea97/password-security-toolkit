"""
Password Pattern Detection Module

Detects common weak password patterns including:
- Common password strings
- Sequential characters
- Repeated characters
- Keyboard patterns
"""

from typing import List

# Top 20 most common password patterns
COMMON_PATTERNS: List[str] = [
    "password",
    "123456",
    "qwerty",
    "abc123",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
    "master",
    "admin",
    "login",
    "passw0rd",
    "password1",
    "123456789",
    "12345678",
    "iloveyou",
    "princess",
    "trustno1",
    "superman",
    "baseball",
]

# Common keyboard walk patterns
KEYBOARD_PATTERNS: List[str] = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "qazwsx",
    "123456",
    "!@#$%^",
    "asdf",
    "qwer",
    "zxcv",
]


def has_common_pattern(password: str) -> bool:
    """
    Check if password contains a common weak pattern.

    Compares against a list of well-known weak passwords
    and common patterns (case-insensitive).

    Args:
        password: The password to check

    Returns:
        True if password contains a common pattern, False otherwise

    Examples:
        >>> has_common_pattern("password123")
        True
        >>> has_common_pattern("MySecureP@ss")
        False
    """
    if not password:
        return False

    password_lower = password.lower()

    # Check if password contains any common pattern
    for pattern in COMMON_PATTERNS:
        if pattern in password_lower:
            return True

    return False


def has_sequential_chars(password: str, min_length: int = 3) -> bool:
    """
    Detect sequential characters in password.

    Finds sequences like:
    - Alphabetic: "abc", "xyz", "ABC"
    - Numeric: "123", "789", "012"

    Args:
        password: The password to check
        min_length: Minimum length of sequence to detect (default: 3)

    Returns:
        True if sequential characters found, False otherwise

    Examples:
        >>> has_sequential_chars("abc123")
        True
        >>> has_sequential_chars("a1b2c3")
        False
    """
    if not password or len(password) < min_length:
        return False

    # Check for sequential characters
    for i in range(len(password) - min_length + 1):
        # Get a substring of min_length
        substring = password[i : i + min_length]

        # Check if all characters are sequential
        is_sequential = True
        for j in range(len(substring) - 1):
            # Check if next character's ord value is exactly 1 more than current
            if ord(substring[j + 1]) != ord(substring[j]) + 1:
                is_sequential = False
                break

        if is_sequential:
            return True

        # Also check reverse sequential (e.g., "cba", "321")
        is_reverse_sequential = True
        for j in range(len(substring) - 1):
            if ord(substring[j + 1]) != ord(substring[j]) - 1:
                is_reverse_sequential = False
                break

        if is_reverse_sequential:
            return True

    return False


def has_repeated_chars(password: str, min_repeats: int = 3) -> bool:
    """
    Detect repeated characters in password.

    Finds patterns like:
    - "aaa", "111", "!!!"
    - "aaaa", "0000"

    Args:
        password: The password to check
        min_repeats: Minimum number of repetitions (default: 3)

    Returns:
        True if repeated characters found, False otherwise

    Examples:
        >>> has_repeated_chars("passswword")
        True
        >>> has_repeated_chars("password")
        False
    """
    if not password or len(password) < min_repeats:
        return False

    # Check for repeated characters
    for i in range(len(password) - min_repeats + 1):
        # Get a character and check if it repeats min_repeats times
        char = password[i]
        is_repeated = True

        for j in range(1, min_repeats):
            if i + j >= len(password) or password[i + j] != char:
                is_repeated = False
                break

        if is_repeated:
            return True

    return False


def is_keyboard_pattern(password: str) -> bool:
    """
    Detect keyboard walk patterns.

    Checks for common sequences from keyboard layout:
    - QWERTY row patterns
    - Adjacent key patterns

    Args:
        password: The password to check

    Returns:
        True if keyboard pattern detected, False otherwise

    Examples:
        >>> is_keyboard_pattern("qwerty123")
        True
        >>> is_keyboard_pattern("random5key")
        False
    """
    if not password:
        return False

    password_lower = password.lower()

    # Check if password contains any keyboard pattern
    for pattern in KEYBOARD_PATTERNS:
        if pattern in password_lower:
            return True

    return False
