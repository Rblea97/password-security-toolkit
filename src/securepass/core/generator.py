"""
Secure Password Generator Module

Generates cryptographically secure random passwords using
the secrets module (NOT the random module).
"""

import secrets
import string
from typing import Optional


# Character set constants
LOWERCASE = string.ascii_lowercase  # abcdefghijklmnopqrstuvwxyz
UPPERCASE = string.ascii_uppercase  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
DIGITS = string.digits              # 0123456789
SYMBOLS = string.punctuation        # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

# Ambiguous characters that can be confused
AMBIGUOUS = "0O1lI"


def generate_password(
    length: int = 16,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    avoid_ambiguous: bool = False
) -> str:
    """
    Generate a cryptographically secure random password.
    
    Uses the secrets module to ensure cryptographic randomness,
    which is suitable for security-sensitive applications.
    
    SECURITY NOTE: This function uses secrets.choice(), NOT random.choice()
    
    Args:
        length: Password length (default: 16, min: 8, max: 128)
        use_lowercase: Include lowercase letters (default: True)
        use_uppercase: Include uppercase letters (default: True)
        use_digits: Include digits (default: True)
        use_symbols: Include symbols/punctuation (default: True)
        avoid_ambiguous: Exclude ambiguous characters like 0/O, 1/l/I (default: False)
        
    Returns:
        Cryptographically secure random password
        
    Raises:
        ValueError: If invalid parameters provided
        
    Examples:
        >>> len(generate_password())
        16
        >>> len(generate_password(length=20))
        20
        >>> pwd = generate_password(use_symbols=False)
        >>> any(c in string.punctuation for c in pwd)
        False
        
    Security:
        - Uses secrets.choice() for cryptographic randomness
        - Ensures at least one character from each selected set
        - Suitable for password generation
    """
    # Validate length
    if not isinstance(length, int):
        raise ValueError("Length must be an integer")
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")
    if length > 128:
        raise ValueError("Password length must not exceed 128 characters")
    
    # Build character pool based on parameters
    char_pool = ""
    required_chars = []
    
    if use_lowercase:
        chars = LOWERCASE
        if avoid_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_uppercase:
        chars = UPPERCASE
        if avoid_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_digits:
        chars = DIGITS
        if avoid_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_symbols:
        char_pool += SYMBOLS
        required_chars.append(secrets.choice(SYMBOLS))
    
    # Validate at least one character set is selected
    if not char_pool:
        raise ValueError("At least one character set must be selected")
    
    # Generate password
    # First, ensure we have at least one char from each selected set
    password_chars = required_chars.copy()
    
    # Fill remaining length with random characters
    remaining_length = length - len(required_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(char_pool))
    
    # Shuffle the password to avoid predictable patterns
    # (required chars at the start)
    # Use secrets.SystemRandom for cryptographically secure shuffle
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_chars)
    
    return ''.join(password_chars)
