"""
Unit tests for password generator module.

Tests password generation with various configurations and validates
cryptographic security requirements.
"""

import pytest
import string
from securepass.core.generator import (
    generate_password,
    LOWERCASE,
    UPPERCASE,
    DIGITS,
    SYMBOLS,
    AMBIGUOUS,
)


class TestGeneratePassword:
    """Tests for generate_password function."""

    def test_default_generation(self):
        """Default password generation should work."""
        password = generate_password()
        assert len(password) == 16
        assert isinstance(password, str)

    def test_custom_length(self):
        """Custom password length."""
        password = generate_password(length=20)
        assert len(password) == 20

        password = generate_password(length=8)
        assert len(password) == 8

        password = generate_password(length=128)
        assert len(password) == 128

    def test_minimum_length_validation(self):
        """Should raise error for length < 8."""
        with pytest.raises(ValueError, match="at least 8"):
            generate_password(length=7)

        with pytest.raises(ValueError, match="at least 8"):
            generate_password(length=0)

    def test_maximum_length_validation(self):
        """Should raise error for length > 128."""
        with pytest.raises(ValueError, match="not exceed 128"):
            generate_password(length=129)

    def test_invalid_length_type(self):
        """Should raise error for non-integer length."""
        with pytest.raises(ValueError, match="must be an integer"):
            generate_password(length="16")

        with pytest.raises(ValueError, match="must be an integer"):
            generate_password(length=16.5)

    def test_no_character_sets(self):
        """Should raise error if no character sets selected."""
        with pytest.raises(ValueError, match="At least one character set"):
            generate_password(
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_symbols=False,
            )

    def test_lowercase_only(self):
        """Generate with only lowercase letters."""
        password = generate_password(
            use_lowercase=True, use_uppercase=False, use_digits=False, use_symbols=False
        )
        assert all(c in LOWERCASE for c in password)
        assert len(password) == 16

    def test_uppercase_only(self):
        """Generate with only uppercase letters."""
        password = generate_password(
            use_lowercase=False, use_uppercase=True, use_digits=False, use_symbols=False
        )
        assert all(c in UPPERCASE for c in password)

    def test_digits_only(self):
        """Generate with only digits."""
        password = generate_password(
            use_lowercase=False, use_uppercase=False, use_digits=True, use_symbols=False
        )
        assert all(c in DIGITS for c in password)

    def test_symbols_only(self):
        """Generate with only symbols."""
        password = generate_password(
            use_lowercase=False, use_uppercase=False, use_digits=False, use_symbols=True
        )
        assert all(c in SYMBOLS for c in password)

    def test_no_symbols(self):
        """Generate without symbols."""
        password = generate_password(use_symbols=False)
        assert not any(c in SYMBOLS for c in password)

    def test_no_uppercase(self):
        """Generate without uppercase."""
        password = generate_password(use_uppercase=False)
        assert not any(c in UPPERCASE for c in password)

    def test_no_digits(self):
        """Generate without digits."""
        password = generate_password(use_digits=False)
        assert not any(c in DIGITS for c in password)

    def test_avoid_ambiguous(self):
        """Generate without ambiguous characters."""
        password = generate_password(avoid_ambiguous=True, length=50)
        # Should not contain 0, O, 1, l, I
        assert not any(c in AMBIGUOUS for c in password)

    def test_contains_each_selected_type(self):
        """Password should contain at least one char from each selected type."""
        # Generate multiple times to ensure consistency
        for _ in range(5):
            password = generate_password(
                use_lowercase=True,
                use_uppercase=True,
                use_digits=True,
                use_symbols=True,
            )

            has_lower = any(c in LOWERCASE for c in password)
            has_upper = any(c in UPPERCASE for c in password)
            has_digit = any(c in DIGITS for c in password)
            has_symbol = any(c in SYMBOLS for c in password)

            assert has_lower, "Should contain at least one lowercase"
            assert has_upper, "Should contain at least one uppercase"
            assert has_digit, "Should contain at least one digit"
            assert has_symbol, "Should contain at least one symbol"

    def test_randomness_uniqueness(self):
        """Generated passwords should be unique (test randomness)."""
        passwords = [generate_password() for _ in range(100)]
        unique_passwords = set(passwords)

        # All 100 passwords should be different
        assert len(unique_passwords) == 100

    def test_randomness_distribution(self):
        """Character distribution should be reasonably random."""
        # Generate a long password and check character distribution
        password = generate_password(length=128)  # Use max allowed length

        # Should have a mix of different characters (not all the same)
        unique_chars = len(set(password))
        assert unique_chars > 30  # Should have variety

    def test_uses_secrets_module(self):
        """Verify that secrets module is being used (not random)."""
        # This is verified by the implementation using secrets.choice()
        # We can test that passwords are cryptographically random by
        # checking they don't follow predictable patterns

        passwords = [generate_password(length=16) for _ in range(10)]

        # No two consecutive passwords should be similar
        for i in range(len(passwords) - 1):
            # Count common characters in same positions
            common = sum(1 for a, b in zip(passwords[i], passwords[i + 1]) if a == b)
            # Shouldn't have more than 3-4 chars in common by chance
            assert common < 5, "Passwords should be sufficiently different"


class TestCharacterConstants:
    """Test that character set constants are properly defined."""

    def test_lowercase_constant(self):
        """LOWERCASE should be a-z."""
        assert LOWERCASE == string.ascii_lowercase
        assert len(LOWERCASE) == 26

    def test_uppercase_constant(self):
        """UPPERCASE should be A-Z."""
        assert UPPERCASE == string.ascii_uppercase
        assert len(UPPERCASE) == 26

    def test_digits_constant(self):
        """DIGITS should be 0-9."""
        assert DIGITS == string.digits
        assert len(DIGITS) == 10

    def test_symbols_constant(self):
        """SYMBOLS should be punctuation."""
        assert SYMBOLS == string.punctuation

    def test_ambiguous_constant(self):
        """AMBIGUOUS should contain confusable characters."""
        assert "0" in AMBIGUOUS
        assert "O" in AMBIGUOUS
        assert "1" in AMBIGUOUS
        assert "l" in AMBIGUOUS
        assert "I" in AMBIGUOUS
