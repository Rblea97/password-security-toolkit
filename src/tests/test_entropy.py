"""
Unit tests for entropy calculator module.

Tests pool size detection, entropy calculation, and crack time estimation.
"""

import pytest
from securepass.core.entropy import (
    get_character_pool_size,
    calculate_entropy,
    estimate_crack_time,
    _format_time,
)


class TestCharacterPoolSize:
    """Tests for get_character_pool_size function."""

    def test_empty_password(self):
        """Empty password should return 0."""
        assert get_character_pool_size("") == 0

    def test_lowercase_only(self):
        """Only lowercase letters should return 26."""
        assert get_character_pool_size("password") == 26
        assert get_character_pool_size("abcdefghijklmnopqrstuvwxyz") == 26

    def test_uppercase_only(self):
        """Only uppercase letters should return 26."""
        assert get_character_pool_size("PASSWORD") == 26
        assert get_character_pool_size("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 26

    def test_digits_only(self):
        """Only digits should return 10."""
        assert get_character_pool_size("1234567890") == 10

    def test_symbols_only(self):
        """Only symbols should return 32."""
        assert get_character_pool_size("!@#$%^&*()") == 32

    def test_mixed_lower_upper(self):
        """Lowercase + uppercase should return 52."""
        assert get_character_pool_size("Password") == 52

    def test_mixed_all_types(self):
        """All character types should return 94."""
        assert get_character_pool_size("P@ssw0rd!") == 94
        assert get_character_pool_size("Abc123!@#") == 94


class TestCalculateEntropy:
    """Tests for calculate_entropy function."""

    def test_empty_password(self):
        """Empty password should return (0.0, 0)."""
        entropy, pool = calculate_entropy("")
        assert entropy == 0.0
        assert pool == 0

    def test_single_char(self):
        """Single character password."""
        entropy, pool = calculate_entropy("a")
        assert pool == 26
        assert entropy > 0

    def test_known_entropy_lowercase(self):
        """Test entropy calculation for lowercase password."""
        # "password" = 8 chars, pool size 26
        # Entropy = log2(26) * 8 ≈ 37.6 bits
        entropy, pool = calculate_entropy("password")
        assert pool == 26
        assert 37.0 < entropy < 38.0

    def test_known_entropy_mixed(self):
        """Test entropy calculation for mixed password."""
        # "P@ssw0rd" = 8 chars, pool size 94
        # Entropy = log2(94) * 8 ≈ 52.4 bits
        entropy, pool = calculate_entropy("P@ssw0rd")
        assert pool == 94
        assert 52.0 < entropy < 53.0

    def test_very_long_password(self):
        """Very long password should have high entropy."""
        long_pwd = "a" * 128
        entropy, pool = calculate_entropy(long_pwd)
        assert pool == 26
        assert entropy > 500  # log2(26) * 128 ≈ 601


class TestEstimateCrackTime:
    """Tests for estimate_crack_time function."""

    def test_zero_entropy(self):
        """Zero entropy should return 'instant'."""
        times = estimate_crack_time(0)
        assert times["online_attack_100_per_second"] == "instant"
        assert times["offline_attack_10B_per_second"] == "instant"

    def test_negative_entropy(self):
        """Negative entropy should return 'instant'."""
        times = estimate_crack_time(-10)
        assert times["online_attack_100_per_second"] == "instant"
        assert times["offline_attack_10B_per_second"] == "instant"

    def test_low_entropy(self):
        """Low entropy (20 bits) should crack quickly."""
        times = estimate_crack_time(20)
        # 2^20 = 1,048,576 combinations
        # Online: 1,048,576 / 100 = 10,485 seconds ≈ 2.9 hours
        # Offline: 1,048,576 / 10B = instant
        assert (
            "hours" in times["online_attack_100_per_second"]
            or "minutes" in times["online_attack_100_per_second"]
        )
        assert (
            "instant" in times["offline_attack_10B_per_second"]
            or "seconds" in times["offline_attack_10B_per_second"]
        )

    def test_medium_entropy(self):
        """Medium entropy (40 bits) should take longer."""
        times = estimate_crack_time(40)
        # 2^40 = ~1 trillion combinations
        assert (
            "years" in times["online_attack_100_per_second"]
            or "centuries" in times["online_attack_100_per_second"]
        )

    def test_high_entropy(self):
        """High entropy (80 bits) should be very secure."""
        times = estimate_crack_time(80)
        # 2^80 = massive number
        assert (
            "years" in times["online_attack_100_per_second"]
            or "centuries" in times["online_attack_100_per_second"]
            or "millennia" in times["online_attack_100_per_second"]
        )


class TestFormatTime:
    """Tests for _format_time helper function."""

    def test_instant(self):
        """Very small values should be 'instant'."""
        assert _format_time(0) == "instant"
        assert _format_time(0.0001) == "instant"

    def test_seconds(self):
        """Seconds range."""
        assert "seconds" in _format_time(1.5)
        assert "seconds" in _format_time(30)

    def test_minutes(self):
        """Minutes range."""
        assert "minutes" in _format_time(120)  # 2 minutes

    def test_hours(self):
        """Hours range."""
        assert "hours" in _format_time(7200)  # 2 hours

    def test_days(self):
        """Days range."""
        assert "days" in _format_time(172800)  # 2 days

    def test_years(self):
        """Years range."""
        assert "years" in _format_time(63072000)  # 2 years

    def test_centuries(self):
        """Centuries range."""
        assert "centuries" in _format_time(6307200000)  # 200 years
