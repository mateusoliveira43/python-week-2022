"""Command to list beers stored in the service."""

from typing import Optional

import typer

from beerlog.cli.utils import parse_result
from beerlog.core import get_beers_from_database


def list_beers(style: Optional[str] = typer.Argument(None)) -> None:
    """
    List beers stored in service's database.

    List all beers, if no style is passed, else, list all beers of the selected
    style.

    Parameters
    ----------
    style : Optional[str], optional
        Filter of beer's style to be applied, by default typer.Argument(None)

    """
    parse_result(get_beers_from_database(style=style))
