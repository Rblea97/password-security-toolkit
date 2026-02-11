"""
Wordlist Management Module

Loads and checks passwords against a dictionary of common passwords.
"""

from typing import Set
import os


# Module-level cache for wordlist (loaded once)
_WORDLIST_CACHE: Set[str] = None


def load_wordlist() -> Set[str]:
    """
    Load common passwords from data file.
    
    Reads the common_passwords.txt file and caches it in memory
    for fast O(1) lookup operations.
    
    Returns:
        Set of common passwords (all lowercase)
        
    Raises:
        FileNotFoundError: If common_passwords.txt is not found
    """
    global _WORDLIST_CACHE
    
    # Return cached wordlist if already loaded
    if _WORDLIST_CACHE is not None:
        return _WORDLIST_CACHE
    
    # Determine the path to the data file
    # The data directory is at /home/claude/src/data/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up from securepass/utils to src, then to data
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(current_dir)),
        'data',
        'common_passwords.txt'
    )
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Common passwords file not found at: {data_path}\n"
            "Please ensure data/common_passwords.txt exists."
        )
    
    # Load wordlist
    wordlist = set()
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip whitespace and convert to lowercase
            word = line.strip().lower()
            if word:  # Skip empty lines
                wordlist.add(word)
    
    # Cache the wordlist
    _WORDLIST_CACHE = wordlist
    
    return wordlist


def contains_dictionary_word(password: str) -> bool:
    """
    Check if password is or contains a common dictionary word.
    
    Performs case-insensitive matching against the common passwords
    wordlist.
    
    Args:
        password: The password to check
        
    Returns:
        True if password matches a dictionary word, False otherwise
        
    Examples:
        >>> contains_dictionary_word("password")
        True
        >>> contains_dictionary_word("PASSWORD")
        True
        >>> contains_dictionary_word("MyP@ssw0rd")
        False
        >>> contains_dictionary_word("xK9#mQ2$pL")
        False
    """
    if not password:
        return False
    
    try:
        wordlist = load_wordlist()
    except FileNotFoundError:
        # If wordlist file is missing, can't check
        # Return False to avoid blocking password analysis
        return False
    
    password_lower = password.lower()
    
    # Check exact match
    if password_lower in wordlist:
        return True
    
    # Check if password contains any word from the wordlist
    # (e.g., "password123" contains "password")
    for word in wordlist:
        if len(word) >= 4 and word in password_lower:  # Only check words 4+ chars
            return True
    
    return False
