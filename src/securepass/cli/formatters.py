"""
CLI Output Formatters Module

Formats password analysis results for display in terminal with colors.
"""

from typing import List
import json

try:
    from colorama import init, Fore, Style

    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

    # Fallback: no colors
    class Fore:  # type: ignore[no-redef]
        RED = YELLOW = GREEN = BLUE = CYAN = WHITE = RESET = ""

    class Style:  # type: ignore[no-redef]
        BRIGHT = DIM = RESET_ALL = ""


from ..models.analysis import PasswordAnalysis


def _get_color_for_score(score: int) -> str:
    """
    Get color code for password strength score.

    Color mapping:
    - 0-39 (weak): Red
    - 40-69 (moderate): Yellow
    - 70-89 (strong): Green
    - 90-100 (very strong): Blue

    Args:
        score: Strength score (0-100)

    Returns:
        Colorama color code
    """
    if score < 40:
        return Fore.RED
    elif score < 70:
        return Fore.YELLOW
    elif score < 90:
        return Fore.GREEN
    else:
        return Fore.BLUE


def format_analysis_text(analysis: PasswordAnalysis, verbose: bool = False) -> str:
    """
    Format analysis as colored terminal output.

    Creates a human-readable report with:
    - Colored strength score
    - Entropy and crack time estimates
    - Criteria checklist with ✓/✗
    - Breach status
    - Recommendations

    Args:
        analysis: PasswordAnalysis object
        verbose: Show additional details (default: False)

    Returns:
        Formatted string ready for terminal display
    """
    color = _get_color_for_score(analysis.strength_score)

    # Header
    output = []
    output.append("")
    output.append(f"{Style.BRIGHT}{'='*70}")
    output.append(f"{Style.BRIGHT}  PASSWORD STRENGTH ANALYSIS")
    output.append(f"{Style.BRIGHT}{'='*70}")
    output.append("")

    # Strength score with color
    rating_display = analysis.strength_rating.replace("_", " ").upper()
    output.append(
        f"{Style.BRIGHT}Strength Score: {color}{analysis.strength_score}/100 [{rating_display}]{Style.RESET_ALL}"
    )
    output.append("")

    # Entropy and metrics
    output.append(f"{Style.BRIGHT}Entropy Analysis:")
    output.append(f"  Entropy: {analysis.entropy_bits:.1f} bits")
    output.append(f"  Character Pool: {analysis.character_pool_size} characters")
    output.append(f"  Password Length: {analysis.length} characters")
    output.append("")

    # Crack time estimates
    output.append(f"{Style.BRIGHT}Estimated Crack Time:")
    online_time = analysis.estimated_crack_time.get(
        "online_attack_100_per_second", "N/A"
    )
    offline_time = analysis.estimated_crack_time.get(
        "offline_attack_10B_per_second", "N/A"
    )
    output.append(f"  Online Attack (100/sec):  {online_time}")
    output.append(f"  Offline Attack (10B/sec): {offline_time}")
    output.append("")

    # Criteria checklist
    output.append(f"{Style.BRIGHT}Security Criteria:")
    criteria_labels = {
        "min_length": "Minimum length (12+ characters)",
        "has_lowercase": "Contains lowercase letters",
        "has_uppercase": "Contains uppercase letters",
        "has_digits": "Contains digits",
        "has_symbols": "Contains symbols",
        "no_common_patterns": "No common patterns",
        "no_dictionary_words": "Not a dictionary word",
        "no_sequential_chars": "No sequential characters",
    }

    for key, label in criteria_labels.items():
        passed = analysis.criteria_met.get(key, False)
        if passed:
            icon = f"{Fore.GREEN}✓{Style.RESET_ALL}"
        else:
            icon = f"{Fore.RED}✗{Style.RESET_ALL}"
        output.append(f"  {icon} {label}")
    output.append("")

    # Breach status
    output.append(f"{Style.BRIGHT}Breach Database Check:")
    if analysis.breach_status.get("checked", False):
        if analysis.breach_status.get("found", False):
            count = analysis.breach_status.get("occurrence_count", 0)
            output.append(
                f"  {Fore.RED}⚠️  FOUND in {count:,} data breaches!{Style.RESET_ALL}"
            )
            output.append(
                f"  {Fore.RED}    ⚠️  Change this password immediately!{Style.RESET_ALL}"
            )
        else:
            output.append(
                f"  {Fore.GREEN}✓ Not found in breach database{Style.RESET_ALL}"
            )
    else:
        output.append(f"  {Fore.YELLOW}⚠ Breach check skipped{Style.RESET_ALL}")
    output.append("")

    # Recommendations
    if analysis.recommendations:
        output.append(f"{Style.BRIGHT}Recommendations:")
        for rec in analysis.recommendations:
            output.append(f"  • {rec}")
        output.append("")

    # Verbose mode: additional details
    if verbose:
        output.append(f"{Style.BRIGHT}Additional Details:")
        output.append(f"  Password Hash (SHA-256): {analysis.password_hash[:16]}...")
        output.append(f"  Analysis Timestamp: {analysis.timestamp}")
        output.append("")

    output.append("=" * 70)
    output.append("")

    return "\n".join(output)


def format_analysis_json(analysis: PasswordAnalysis, pretty: bool = True) -> str:
    """
    Format analysis as JSON string.

    Args:
        analysis: PasswordAnalysis object
        pretty: Use indentation for readability (default: True)

    Returns:
        JSON string representation
    """
    indent = 2 if pretty else None
    return json.dumps(analysis.to_dict(), indent=indent)


def format_batch_summary(results: List[PasswordAnalysis]) -> str:
    """
    Generate summary report for batch analysis.

    Shows:
    - Total passwords analyzed
    - Count by rating category
    - Weakest passwords (top 5)
    - Breach statistics

    Args:
        results: List of PasswordAnalysis objects

    Returns:
        Formatted summary string
    """
    if not results:
        return "No passwords analyzed."

    output = []
    output.append("")
    output.append(f"{Style.BRIGHT}{'='*70}")
    output.append(f"{Style.BRIGHT}  BATCH ANALYSIS SUMMARY")
    output.append(f"{Style.BRIGHT}{'='*70}")
    output.append("")

    # Total count
    total = len(results)
    output.append(f"{Style.BRIGHT}Total Passwords Analyzed: {total}")
    output.append("")

    # Count by rating
    ratings = {"weak": 0, "moderate": 0, "strong": 0, "very_strong": 0}
    breached_count = 0

    for result in results:
        ratings[result.strength_rating] += 1
        if result.breach_status.get("found", False):
            breached_count += 1

    output.append(f"{Style.BRIGHT}Strength Distribution:")
    output.append(
        f"  {Fore.RED}Weak:        {ratings['weak']:3d} ({ratings['weak']/total*100:.1f}%){Style.RESET_ALL}"
    )
    output.append(
        f"  {Fore.YELLOW}Moderate:    {ratings['moderate']:3d} ({ratings['moderate']/total*100:.1f}%){Style.RESET_ALL}"
    )
    output.append(
        f"  {Fore.GREEN}Strong:      {ratings['strong']:3d} ({ratings['strong']/total*100:.1f}%){Style.RESET_ALL}"
    )
    output.append(
        f"  {Fore.BLUE}Very Strong: {ratings['very_strong']:3d} ({ratings['very_strong']/total*100:.1f}%){Style.RESET_ALL}"
    )
    output.append("")

    # Breach statistics
    output.append(f"{Style.BRIGHT}Breach Statistics:")
    output.append(
        f"  Passwords in breaches: {Fore.RED}{breached_count}{Style.RESET_ALL} ({breached_count/total*100:.1f}%)"
    )
    output.append("")

    # Top 5 weakest passwords
    sorted_results = sorted(results, key=lambda x: x.strength_score)
    weakest = sorted_results[: min(5, len(sorted_results))]

    output.append(f"{Style.BRIGHT}Weakest Passwords (Top 5):")
    for i, result in enumerate(weakest, 1):
        color = _get_color_for_score(result.strength_score)
        hash_preview = result.password_hash[:12] + "..."
        output.append(
            f"  {i}. Score: {color}{result.strength_score:3d}{Style.RESET_ALL} | Hash: {hash_preview}"
        )
    output.append("")

    # Average metrics
    avg_score = sum(r.strength_score for r in results) / total
    avg_entropy = sum(r.entropy_bits for r in results) / total
    avg_length = sum(r.length for r in results) / total

    output.append(f"{Style.BRIGHT}Average Metrics:")
    output.append(f"  Average Score:   {avg_score:.1f}/100")
    output.append(f"  Average Entropy: {avg_entropy:.1f} bits")
    output.append(f"  Average Length:  {avg_length:.1f} characters")
    output.append("")

    output.append("=" * 70)
    output.append("")

    return "\n".join(output)
