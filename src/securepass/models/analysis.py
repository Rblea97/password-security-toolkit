"""
Password Analysis Data Models

Defines the data structures for password analysis results.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Union
from datetime import datetime
import json


@dataclass
class PasswordAnalysis:
    """
    Complete password analysis result.

    Contains all metrics from password strength evaluation including:
    - Strength score and rating
    - Entropy calculations
    - Criteria evaluation
    - Breach status
    - Recommendations
    """

    password_hash: str  # SHA-256 hash (for audit trails only, never plaintext)
    timestamp: str  # ISO 8601 datetime
    strength_score: int  # 0-100
    strength_rating: str  # weak, moderate, strong, very_strong
    length: int  # Password length
    entropy_bits: float  # Shannon entropy in bits
    character_pool_size: int  # Detected character pool size
    criteria_met: Dict[str, bool]  # Which criteria passed/failed
    breach_status: Dict[str, Union[bool, int]]  # Breach check results
    recommendations: List[str]  # Improvement suggestions
    estimated_crack_time: Dict[str, str]  # Crack time estimates

    def to_dict(self) -> dict:
        """
        Convert analysis to dictionary for JSON export.

        Returns:
            Dictionary representation of all analysis data
        """
        return {
            "password_hash": self.password_hash,
            "timestamp": self.timestamp,
            "strength_score": self.strength_score,
            "strength_rating": self.strength_rating,
            "length": self.length,
            "entropy_bits": self.entropy_bits,
            "character_pool_size": self.character_pool_size,
            "criteria_met": self.criteria_met,
            "breach_status": self.breach_status,
            "recommendations": self.recommendations,
            "estimated_crack_time": self.estimated_crack_time,
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert analysis to JSON string.

        Args:
            indent: JSON indentation level (default: 2)

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)

    def to_csv_row(self) -> List[str]:
        """
        Convert analysis to CSV row format.

        Returns:
            List of strings representing CSV row values
        """
        return [
            self.password_hash,
            self.timestamp,
            str(self.strength_score),
            self.strength_rating,
            str(self.length),
            f"{self.entropy_bits:.2f}",
            str(self.character_pool_size),
            str(self.criteria_met.get("min_length", False)),
            str(self.criteria_met.get("has_lowercase", False)),
            str(self.criteria_met.get("has_uppercase", False)),
            str(self.criteria_met.get("has_digits", False)),
            str(self.criteria_met.get("has_symbols", False)),
            str(self.criteria_met.get("no_common_patterns", False)),
            str(self.criteria_met.get("no_dictionary_words", False)),
            str(self.criteria_met.get("no_sequential_chars", False)),
            str(self.breach_status.get("found", False)),
            str(self.breach_status.get("occurrence_count", 0)),
            self.estimated_crack_time.get("online_attack_100_per_second", ""),
            self.estimated_crack_time.get("offline_attack_10B_per_second", ""),
        ]

    @staticmethod
    def csv_header() -> List[str]:
        """
        Get CSV header row.

        Returns:
            List of column names for CSV export
        """
        return [
            "password_hash",
            "timestamp",
            "strength_score",
            "strength_rating",
            "length",
            "entropy_bits",
            "character_pool_size",
            "min_length",
            "has_lowercase",
            "has_uppercase",
            "has_digits",
            "has_symbols",
            "no_common_patterns",
            "no_dictionary_words",
            "no_sequential_chars",
            "breached",
            "breach_count",
            "crack_time_online",
            "crack_time_offline",
        ]

    def __str__(self) -> str:
        """
        Human-readable string representation.

        Returns:
            Formatted string with key analysis metrics
        """
        return (
            f"Password Analysis\n"
            f"  Score: {self.strength_score}/100 ({self.strength_rating.upper()})\n"
            f"  Length: {self.length} characters\n"
            f"  Entropy: {self.entropy_bits:.1f} bits\n"
            f"  Breached: {self.breach_status.get('found', False)}"
        )
