"""
Unit tests for pattern detection module.

Tests common pattern detection, sequential characters, repeated characters,
and keyboard patterns.
"""

import pytest
from securepass.utils.patterns import (
    has_common_pattern,
    has_sequential_chars,
    has_repeated_chars,
    is_keyboard_pattern,
    COMMON_PATTERNS,
    KEYBOARD_PATTERNS,
)


class TestHasCommonPattern:
    """Tests for has_common_pattern function."""

    def test_empty_password(self):
        """Empty password should return False."""
        assert has_common_pattern("") is False

    def test_exact_match(self):
        """Exact match of common pattern."""
        assert has_common_pattern("password") is True
        assert has_common_pattern("123456") is True
        assert has_common_pattern("qwerty") is True

    def test_case_insensitive(self):
        """Should be case-insensitive."""
        assert has_common_pattern("PASSWORD") is True
        assert has_common_pattern("PaSsWoRd") is True

    def test_pattern_within_password(self):
        """Pattern contained within larger password."""
        assert has_common_pattern("password123") is True
        assert has_common_pattern("mypassword") is True
        assert has_common_pattern("123456789") is True

    def test_no_common_pattern(self):
        """Strong password with no common patterns."""
        assert has_common_pattern("K7$mP9@nQ2") is False
        assert has_common_pattern("xK9#mQ2$pL") is False


class TestHasSequentialChars:
    """Tests for has_sequential_chars function."""

    def test_empty_password(self):
        """Empty password should return False."""
        assert has_sequential_chars("") is False

    def test_too_short(self):
        """Password shorter than min_length should return False."""
        assert has_sequential_chars("ab", min_length=3) is False

    def test_alphabetic_sequence(self):
        """Detect alphabetic sequences."""
        assert has_sequential_chars("abc") is True
        assert has_sequential_chars("xyz") is True
        assert has_sequential_chars("defgh") is True
        assert has_sequential_chars("password_abc_test") is True

    def test_numeric_sequence(self):
        """Detect numeric sequences."""
        assert has_sequential_chars("123") is True
        assert has_sequential_chars("456789") is True
        assert has_sequential_chars("pass123word") is True

    def test_reverse_sequence(self):
        """Detect reverse sequences."""
        assert has_sequential_chars("cba") is True
        assert has_sequential_chars("321") is True
        assert has_sequential_chars("zyx") is True

    def test_uppercase_sequence(self):
        """Detect uppercase sequences."""
        assert has_sequential_chars("ABC") is True
        assert has_sequential_chars("XYZ") is True

    def test_no_sequence(self):
        """No sequential characters."""
        assert has_sequential_chars("a1b2c3") is False
        assert has_sequential_chars("password") is False
        assert has_sequential_chars("K7$mP9@n") is False

    def test_custom_min_length(self):
        """Test with custom minimum length."""
        assert has_sequential_chars("ab", min_length=2) is True
        assert has_sequential_chars("abcd", min_length=4) is True
        assert has_sequential_chars("abc", min_length=4) is False


class TestHasRepeatedChars:
    """Tests for has_repeated_chars function."""

    def test_empty_password(self):
        """Empty password should return False."""
        assert has_repeated_chars("") is False

    def test_too_short(self):
        """Password shorter than min_repeats should return False."""
        assert has_repeated_chars("aa", min_repeats=3) is False

    def test_repeated_letters(self):
        """Detect repeated letters."""
        assert has_repeated_chars("aaa") is True
        assert has_repeated_chars("passsword") is True
        assert has_repeated_chars("hellooo") is True

    def test_repeated_digits(self):
        """Detect repeated digits."""
        assert has_repeated_chars("111") is True
        assert has_repeated_chars("pass000word") is True

    def test_repeated_symbols(self):
        """Detect repeated symbols."""
        assert has_repeated_chars("!!!") is True
        assert has_repeated_chars("pass###word") is True

    def test_no_repetition(self):
        """No repeated characters."""
        assert has_repeated_chars("password") is False
        assert has_repeated_chars("abc123") is False
        assert has_repeated_chars("aabbcc") is False  # Only 2 repeats each

    def test_custom_min_repeats(self):
        """Test with custom minimum repeats."""
        assert has_repeated_chars("aa", min_repeats=2) is True
        assert has_repeated_chars("aaaa", min_repeats=4) is True
        assert has_repeated_chars("aaa", min_repeats=4) is False


class TestIsKeyboardPattern:
    """Tests for is_keyboard_pattern function."""

    def test_empty_password(self):
        """Empty password should return False."""
        assert is_keyboard_pattern("") is False

    def test_qwerty_pattern(self):
        """Detect QWERTY keyboard patterns."""
        assert is_keyboard_pattern("qwerty") is True
        assert is_keyboard_pattern("QWERTY") is True
        assert is_keyboard_pattern("qwerty123") is True

    def test_asdf_pattern(self):
        """Detect ASDF keyboard patterns."""
        assert is_keyboard_pattern("asdfgh") is True
        assert is_keyboard_pattern("asdf") is True

    def test_other_keyboard_patterns(self):
        """Detect other keyboard patterns."""
        assert is_keyboard_pattern("zxcvbn") is True
        assert is_keyboard_pattern("qazwsx") is True

    def test_no_keyboard_pattern(self):
        """No keyboard patterns."""
        assert is_keyboard_pattern("password") is False
        assert is_keyboard_pattern("K7$mP9@n") is False
        assert is_keyboard_pattern("random123") is False


class TestPatternConstants:
    """Test that pattern constants are properly defined."""

    def test_common_patterns_list(self):
        """COMMON_PATTERNS should be a non-empty list."""
        assert isinstance(COMMON_PATTERNS, list)
        assert len(COMMON_PATTERNS) > 0
        assert "password" in COMMON_PATTERNS
        assert "123456" in COMMON_PATTERNS

    def test_keyboard_patterns_list(self):
        """KEYBOARD_PATTERNS should be a non-empty list."""
        assert isinstance(KEYBOARD_PATTERNS, list)
        assert len(KEYBOARD_PATTERNS) > 0
        assert "qwerty" in KEYBOARD_PATTERNS
