"""Command to add a beer to database."""

import typer

from beerlog.cli.utils import parse_result
from beerlog.core import add_beer_to_database


def add(
    name: str,
    style: str,
    flavor: int = typer.Option(...),
    image: int = typer.Option(...),
    cost: int = typer.Option(...),
) -> None:
    """
    Add a new beer to service's database.

    Parameters
    ----------
    name : str
        Beer's name.
    style : str
        Beer's style.
    flavor : int
        Beer's flavor, between 1 and 10, by default typer.Option(...)
    image : int
        Beer's image, between 1 and 10, by default typer.Option(...)
    cost : int
        Beer's cost, between 1 and 10, by default typer.Option(...)

    """
    parse_result(
        add_beer_to_database(
            name=name, style=style, flavor=flavor, image=image, cost=cost
        )
    )
