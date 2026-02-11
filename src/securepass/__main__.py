"""
SecurePass Toolkit - Main CLI Entry Point

Command-line interface for password security analysis.
"""

import sys
import argparse
from .cli.commands import cmd_check, cmd_generate, cmd_batch


VERSION = "1.0.0"


def main() -> int:
    """
    Main CLI entry point.
    
    Parses command-line arguments and routes to appropriate command handler.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Main parser
    parser = argparse.ArgumentParser(
        prog='securepass',
        description='SecurePass Toolkit - Password Security Analysis Suite',
        epilog='For more information, visit: https://github.com/yourusername/securepass-toolkit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'SecurePass Toolkit v{VERSION}'
    )
    
    # Subcommand parsers
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )
    
    # ========================================
    # CHECK command
    # ========================================
    check_parser = subparsers.add_parser(
        'check',
        help='Analyze password strength interactively',
        description='Analyze the strength of a password with detailed metrics and recommendations.'
    )
    
    check_parser.add_argument(
        '--no-breach',
        action='store_true',
        help='Skip breach database checking (faster, offline mode)'
    )
    
    check_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show additional analysis details'
    )
    
    # ========================================
    # GENERATE command
    # ========================================
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate a secure random password',
        description='Generate a cryptographically secure random password with customizable options.'
    )
    
    generate_parser.add_argument(
        '--length', '-l',
        type=int,
        default=16,
        metavar='N',
        help='Password length (default: 16, min: 8, max: 128)'
    )
    
    generate_parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude symbols/punctuation'
    )
    
    generate_parser.add_argument(
        '--no-uppercase',
        action='store_true',
        help='Exclude uppercase letters'
    )
    
    generate_parser.add_argument(
        '--no-digits',
        action='store_true',
        help='Exclude digits'
    )
    
    generate_parser.add_argument(
        '--avoid-ambiguous',
        action='store_true',
        help='Avoid ambiguous characters (0, O, 1, l, I)'
    )
    
    # ========================================
    # BATCH command
    # ========================================
    batch_parser = subparsers.add_parser(
        'batch',
        help='Analyze multiple passwords from a file',
        description='Analyze passwords from a file (one per line) and generate a summary report.'
    )
    
    batch_parser.add_argument(
        'file',
        help='Input file containing passwords (one per line)'
    )
    
    batch_parser.add_argument(
        '--output',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format for export (default: text)'
    )
    
    batch_parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to file'
    )
    
    batch_parser.add_argument(
        '--no-breach',
        action='store_true',
        help='Skip breach database checking (much faster for large batches)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Route to appropriate command handler
    try:
        if args.command == 'check':
            return cmd_check(args)
        elif args.command == 'generate':
            return cmd_generate(args)
        elif args.command == 'batch':
            return cmd_batch(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
