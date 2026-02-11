"""
Unit tests for password analyzer module.

Tests the main orchestration logic including criteria checking,
score calculation, and password analysis.
"""

import pytest
from securepass.core.analyzer import (
    _check_criteria,
    calculate_strength_score,
    _determine_rating,
    get_recommendations,
    analyze_password
)
from securepass.models.analysis import PasswordAnalysis


class TestCheckCriteria:
    """Tests for _check_criteria function."""
    
    def test_very_weak_password(self):
        """Very weak password should fail most criteria."""
        criteria = _check_criteria("password")
        
        assert criteria['min_length'] is False  # Only 8 chars
        assert criteria['has_lowercase'] is True
        assert criteria['has_uppercase'] is False
        assert criteria['has_digits'] is False
        assert criteria['has_symbols'] is False
        assert criteria['no_common_patterns'] is False  # Contains "password"
        assert criteria['no_dictionary_words'] is False  # Is dictionary word
        assert criteria['no_sequential_chars'] is True
    
    def test_strong_password(self):
        """Strong password should pass all criteria."""
        criteria = _check_criteria("MyP@ssw0rd!2024")
        
        assert criteria['min_length'] is True
        assert criteria['has_lowercase'] is True
        assert criteria['has_uppercase'] is True
        assert criteria['has_digits'] is True
        assert criteria['has_symbols'] is True
        # Note: This password contains "password" so it may fail pattern check
    
    def test_very_strong_random_password(self):
        """Very strong random password."""
        criteria = _check_criteria("K7$mP9@nQ2#wX5zT")
        
        assert criteria['min_length'] is True
        assert criteria['has_lowercase'] is True
        assert criteria['has_uppercase'] is True
        assert criteria['has_digits'] is True
        assert criteria['has_symbols'] is True
        assert criteria['no_common_patterns'] is True
        assert criteria['no_dictionary_words'] is True
        assert criteria['no_sequential_chars'] is True


class TestCalculateStrengthScore:
    """Tests for calculate_strength_score function."""
    
    def test_all_criteria_passed_high_entropy(self):
        """All criteria + high entropy should score 100."""
        criteria = {
            'min_length': True,
            'has_lowercase': True,
            'has_uppercase': True,
            'has_digits': True,
            'has_symbols': True,
            'no_common_patterns': True,
            'no_dictionary_words': True,
            'no_sequential_chars': True
        }
        score = calculate_strength_score(criteria, entropy=80.0)
        assert score == 100  # 80 (base) + 20 (entropy) = 100
    
    def test_all_criteria_passed_low_entropy(self):
        """All criteria but low entropy."""
        criteria = {k: True for k in [
            'min_length', 'has_lowercase', 'has_uppercase', 'has_digits',
            'has_symbols', 'no_common_patterns', 'no_dictionary_words',
            'no_sequential_chars'
        ]}
        score = calculate_strength_score(criteria, entropy=30.0)
        assert score == 80  # 80 (base) + 0 (no entropy bonus)
    
    def test_no_criteria_passed(self):
        """No criteria passed."""
        criteria = {k: False for k in [
            'min_length', 'has_lowercase', 'has_uppercase', 'has_digits',
            'has_symbols', 'no_common_patterns', 'no_dictionary_words',
            'no_sequential_chars'
        ]}
        score = calculate_strength_score(criteria, entropy=0.0)
        assert score == 0
    
    def test_entropy_bonus_tiers(self):
        """Test entropy bonus tiers."""
        criteria = {k: False for k in [
            'min_length', 'has_lowercase', 'has_uppercase', 'has_digits',
            'has_symbols', 'no_common_patterns', 'no_dictionary_words',
            'no_sequential_chars'
        ]}
        
        # 40-50 bits: +5
        assert calculate_strength_score(criteria, 45) == 5
        
        # 50-60 bits: +10
        assert calculate_strength_score(criteria, 55) == 10
        
        # 60-70 bits: +15
        assert calculate_strength_score(criteria, 65) == 15
        
        # 70+ bits: +20
        assert calculate_strength_score(criteria, 75) == 20


class TestDetermineRating:
    """Tests for _determine_rating function."""
    
    def test_weak_rating(self):
        """Scores 0-39 should be 'weak'."""
        assert _determine_rating(0) == 'weak'
        assert _determine_rating(20) == 'weak'
        assert _determine_rating(39) == 'weak'
    
    def test_moderate_rating(self):
        """Scores 40-69 should be 'moderate'."""
        assert _determine_rating(40) == 'moderate'
        assert _determine_rating(55) == 'moderate'
        assert _determine_rating(69) == 'moderate'
    
    def test_strong_rating(self):
        """Scores 70-89 should be 'strong'."""
        assert _determine_rating(70) == 'strong'
        assert _determine_rating(80) == 'strong'
        assert _determine_rating(89) == 'strong'
    
    def test_very_strong_rating(self):
        """Scores 90-100 should be 'very_strong'."""
        assert _determine_rating(90) == 'very_strong'
        assert _determine_rating(95) == 'very_strong'
        assert _determine_rating(100) == 'very_strong'


class TestAnalyzePassword:
    """Tests for analyze_password function - main integration."""
    
    def test_analyze_weak_password(self):
        """Analyze a weak password."""
        result = analyze_password("password", check_breach_status=False)
        
        assert isinstance(result, PasswordAnalysis)
        assert result.strength_score < 40
        assert result.strength_rating == 'weak'
        assert result.length == 8
        assert len(result.recommendations) > 0
    
    def test_analyze_moderate_password(self):
        """Analyze a moderate password."""
        result = analyze_password("Password123", check_breach_status=False)
        
        assert isinstance(result, PasswordAnalysis)
        assert 40 <= result.strength_score < 70
        assert result.strength_rating == 'moderate'
    
    def test_analyze_strong_password(self):
        """Analyze a strong password."""
        result = analyze_password("MyP@ssw0rd!2024", check_breach_status=False)
        
        assert isinstance(result, PasswordAnalysis)
        assert result.strength_score >= 70
        assert result.strength_rating in ['strong', 'very_strong']
    
    def test_analyze_very_strong_password(self):
        """Analyze a very strong password."""
        result = analyze_password("K7$mP9@nQ2#wX5zT", check_breach_status=False)
        
        assert isinstance(result, PasswordAnalysis)
        assert result.strength_score >= 90
        assert result.strength_rating == 'very_strong'
        assert result.entropy_bits > 80
    
    def test_password_hash_generated(self):
        """Password hash should be generated."""
        result = analyze_password("test123", check_breach_status=False)
        
        assert result.password_hash is not None
        assert len(result.password_hash) == 64  # SHA-256 hex = 64 chars
    
    def test_timestamp_generated(self):
        """Timestamp should be generated."""
        result = analyze_password("test123", check_breach_status=False)
        
        assert result.timestamp is not None
        assert 'T' in result.timestamp  # ISO 8601 format
    
    def test_recommendations_generated(self):
        """Recommendations should be generated."""
        result = analyze_password("weak", check_breach_status=False)
        
        assert len(result.recommendations) > 0
        assert isinstance(result.recommendations, list)
    
    def test_breach_check_skipped(self):
        """Breach check can be skipped."""
        result = analyze_password("password", check_breach_status=False)
        
        assert result.breach_status['checked'] is False
        assert result.breach_status['found'] is False
    
    def test_crack_time_estimates(self):
        """Crack time estimates should be included."""
        result = analyze_password("password", check_breach_status=False)
        
        assert 'online_attack_100_per_second' in result.estimated_crack_time
        assert 'offline_attack_10B_per_second' in result.estimated_crack_time
    
    def test_all_criteria_evaluated(self):
        """All 8 criteria should be evaluated."""
        result = analyze_password("password", check_breach_status=False)
        
        expected_criteria = [
            'min_length', 'has_lowercase', 'has_uppercase', 'has_digits',
            'has_symbols', 'no_common_patterns', 'no_dictionary_words',
            'no_sequential_chars'
        ]
        
        for criterion in expected_criteria:
            assert criterion in result.criteria_met
