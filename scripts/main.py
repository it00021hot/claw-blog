"""
CLI entry point for the article fetcher.
"""
import argparse
import asyncio
import logging
import sys
from typing import Optional

from scripts.fetch_articles import main as fetch_main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch articles from GitHub and technical blogs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/main.py                    # Fetch all articles
  python scripts/main.py --tech              # Fetch only to tech directory
  python scripts/main.py --fiction           # Fetch only to fiction directory
  python scripts/main.py --dry-run            # Simulate without saving files
  python scripts/main.py --verbose            # Show detailed logs
  python scripts/main.py --tech --verbose     # Combine options
        """,
    )

    parser.add_argument(
        "--tech",
        action="store_true",
        help="Fetch only to tech directory (content/tech/)",
    )

    parser.add_argument(
        "--fiction",
        action="store_true",
        help="Fetch only to fiction directory (content/fiction/)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate running without saving files",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args(args)


def main():
    """CLI main function."""
    args = parse_args()

    # Validate arguments
    if args.tech and args.fiction:
        logger.error("Cannot use both --tech and --fiction at the same time")
        sys.exit(1)

    try:
        result = asyncio.run(
            fetch_main(
                tech_only=args.tech,
                fiction_only=args.fiction,
                dry_run=args.dry_run,
                verbose=args.verbose,
            )
        )

        # Exit with error code if there were errors
        if result.error_count > 0:
            logger.warning(f"Completed with {result.error_count} errors")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
