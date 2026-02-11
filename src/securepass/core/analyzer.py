"""
Password Strength Analyzer Module

Main orchestration module that coordinates all password analysis components:
- Entropy calculation
- Pattern detection
- Dictionary checking
- Breach detection
- Recommendation generation
"""

import hashlib
import string
from datetime import datetime
from typing import Dict, List

from ..models.analysis import PasswordAnalysis
from .entropy import calculate_entropy, estimate_crack_time
from .breach import check_breach
from ..utils.patterns import (
    has_common_pattern,
    has_sequential_chars,
    has_repeated_chars,
    is_keyboard_pattern,
)
from ..utils.wordlist import contains_dictionary_word


def _check_criteria(password: str) -> Dict[str, bool]:
    """
    Check password against all security criteria.

    Evaluates 8 criteria from SPECS.md FR-01:
    1. Minimum length (8+ characters, 12+ recommended)
    2. Contains lowercase letters
    3. Contains uppercase letters
    4. Contains digits
    5. Contains symbols
    6. No common patterns
    7. Not a dictionary word
    8. No sequential characters

    Args:
        password: The password to evaluate

    Returns:
        Dictionary mapping criterion names to boolean pass/fail
    """
    criteria = {}

    # Criterion 1: Minimum length (12+ for strong)
    criteria["min_length"] = len(password) >= 12

    # Criterion 2: Contains lowercase
    criteria["has_lowercase"] = any(c in string.ascii_lowercase for c in password)

    # Criterion 3: Contains uppercase
    criteria["has_uppercase"] = any(c in string.ascii_uppercase for c in password)

    # Criterion 4: Contains digits
    criteria["has_digits"] = any(c in string.digits for c in password)

    # Criterion 5: Contains symbols
    criteria["has_symbols"] = any(c in string.punctuation for c in password)

    # Criterion 6: No common patterns
    criteria["no_common_patterns"] = not has_common_pattern(password)

    # Criterion 7: Not a dictionary word
    criteria["no_dictionary_words"] = not contains_dictionary_word(password)

    # Criterion 8: No sequential characters
    criteria["no_sequential_chars"] = not has_sequential_chars(password)

    return criteria


def calculate_strength_score(criteria: Dict[str, bool], entropy: float) -> int:
    """
    Calculate overall password strength score (0-100).

    Scoring algorithm:
    - Base score: 10 points per criterion met (max 80 points)
    - Entropy bonus: Up to 20 points for high entropy
      - 40-50 bits: +5 points
      - 50-60 bits: +10 points
      - 60-70 bits: +15 points
      - 70+ bits: +20 points

    Args:
        criteria: Dictionary of criteria pass/fail results
        entropy: Password entropy in bits

    Returns:
        Integer score from 0 to 100
    """
    # Base score: 10 points per criterion (max 80)
    base_score = sum(10 for passed in criteria.values() if passed)

    # Entropy bonus (max 20 points)
    if entropy >= 70:
        entropy_bonus = 20
    elif entropy >= 60:
        entropy_bonus = 15
    elif entropy >= 50:
        entropy_bonus = 10
    elif entropy >= 40:
        entropy_bonus = 5
    else:
        entropy_bonus = 0

    total_score = base_score + entropy_bonus

    # Cap at 100
    return min(total_score, 100)


def _determine_rating(score: int) -> str:
    """
    Convert numeric score to categorical rating.

    Rating scale:
    - 0-39: weak
    - 40-69: moderate
    - 70-89: strong
    - 90-100: very_strong

    Args:
        score: Strength score (0-100)

    Returns:
        Rating string: 'weak', 'moderate', 'strong', or 'very_strong'
    """
    if score < 40:
        return "weak"
    elif score < 70:
        return "moderate"
    elif score < 90:
        return "strong"
    else:
        return "very_strong"


def get_recommendations(analysis: PasswordAnalysis) -> List[str]:
    """
    Generate actionable improvement recommendations.

    Analyzes which criteria failed and provides specific
    suggestions for strengthening the password.

    Args:
        analysis: PasswordAnalysis object with criteria results

    Returns:
        List of recommendation strings
    """
    recommendations = []
    criteria = analysis.criteria_met

    # Length recommendations
    if not criteria.get("min_length", False):
        if analysis.length < 8:
            recommendations.append(
                "⚠️ CRITICAL: Password is too short. Use at least 8 characters (12+ recommended)"
            )
        elif analysis.length < 12:
            recommendations.append(
                "Increase length to at least 12 characters for better security"
            )

    # Character diversity recommendations
    if not criteria.get("has_lowercase", False):
        recommendations.append("Add lowercase letters (a-z)")

    if not criteria.get("has_uppercase", False):
        recommendations.append("Add uppercase letters (A-Z)")

    if not criteria.get("has_digits", False):
        recommendations.append("Add numbers (0-9)")

    if not criteria.get("has_symbols", False):
        recommendations.append("Add symbols (!@#$%^&* etc.)")

    # Pattern and dictionary recommendations
    if not criteria.get("no_common_patterns", False):
        recommendations.append(
            "⚠️ Contains common pattern (e.g., 'password', '123456'). Use unique password"
        )

    if not criteria.get("no_dictionary_words", False):
        recommendations.append("⚠️ Contains dictionary word. Avoid common words")

    if not criteria.get("no_sequential_chars", False):
        recommendations.append("Avoid sequential characters (e.g., 'abc', '123')")

    # Breach recommendations
    if analysis.breach_status.get("found", False):
        count = analysis.breach_status.get("occurrence_count", 0)
        recommendations.append(
            f"🚨 CRITICAL: Password found in {count:,} data breaches! "
            f"Change this password immediately!"
        )

    # Entropy-based recommendations
    if analysis.entropy_bits < 40:
        recommendations.append(
            "Password entropy is low. Make it longer and more random"
        )

    # If no issues found
    if not recommendations:
        recommendations.append("✓ Password meets security best practices")

    return recommendations


def analyze_password(
    password: str, check_breach_status: bool = True
) -> PasswordAnalysis:
    """
    Perform comprehensive password analysis.

    Orchestrates all password security checks:
    1. Calculate entropy
    2. Check criteria (length, character types, patterns)
    3. Optionally check breach database
    4. Calculate strength score
    5. Generate recommendations

    Args:
        password: The password to analyze
        check_breach_status: Whether to check HIBP API (default: True)

    Returns:
        Complete PasswordAnalysis object with all metrics

    Examples:
        >>> result = analyze_password("password123")
        >>> result.strength_rating
        'weak'
        >>> result.strength_score < 40
        True

        >>> result = analyze_password("K7$mP9@nQ2#wX5")
        >>> result.strength_rating
        'very_strong'
        >>> result.strength_score > 90
        True
    """
    # Generate SHA-256 hash for audit trail (NOT for breach checking)
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Get current timestamp
    timestamp = datetime.now().isoformat()

    # Calculate entropy
    entropy_bits, pool_size = calculate_entropy(password)

    # Check all criteria
    criteria = _check_criteria(password)

    # Calculate strength score
    strength_score = calculate_strength_score(criteria, entropy_bits)

    # Determine rating
    strength_rating = _determine_rating(strength_score)

    # Check breach status (if enabled)
    if check_breach_status:
        try:
            is_breached, breach_count = check_breach(password)
            breach_status = {
                "checked": True,
                "found": is_breached,
                "occurrence_count": breach_count,
            }
        except Exception as e:
            # If breach check fails, continue without it
            breach_status = {"checked": False, "found": False, "occurrence_count": 0}
    else:
        breach_status = {"checked": False, "found": False, "occurrence_count": 0}

    # Estimate crack time
    crack_time = estimate_crack_time(entropy_bits)

    # Create analysis object (without recommendations initially)
    analysis = PasswordAnalysis(
        password_hash=password_hash,
        timestamp=timestamp,
        strength_score=strength_score,
        strength_rating=strength_rating,
        length=len(password),
        entropy_bits=entropy_bits,
        character_pool_size=pool_size,
        criteria_met=criteria,
        breach_status=breach_status,
        recommendations=[],  # Will be filled next
        estimated_crack_time=crack_time,
    )

    # Generate recommendations based on analysis
    analysis.recommendations = get_recommendations(analysis)

    return analysis
