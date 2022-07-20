"""Beerlog CLI implementation."""

from beerlog.config import settings


def main() -> None:
    """Parse user inputs in service CLI."""
    print("Hello from", settings.NAME)
