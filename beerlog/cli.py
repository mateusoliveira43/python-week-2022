"""Beerlog CLI implementation."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from beerlog.core import add_beer_to_database, get_beers_from_database

main = typer.Typer(help="Beer Management Application")

console = Console()


@main.command("add")
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
    flavor : int, optional
        Beer's flavor, by default typer.Option(...)
    image : int, optional
        Beer's image, by default typer.Option(...)
    cost : int, optional
        Beer's cost, by default typer.Option(...)

    """
    response = add_beer_to_database(
        name=name, style=style, flavor=flavor, image=image, cost=cost
    )
    if response:
        print("\N{beer mug} beer added to database")
    # else:
    #     print("\N{no entry} ")


# TODO add filter functionality
# pylint: disable=unused-argument
@main.command("list")
def list_beers(style: Optional[str] = None) -> None:
    """
    List beers stored in service's database.

    Parameters
    ----------
    style : Optional[str], optional
        Beer's style, by default None

    """
    beers = get_beers_from_database()
    table = Table(title="Beerlog :beer_mug:")
    headers = ["id_", "name", "style", "rate", "date"]
    for header in headers:
        table.add_column(header, style="magenta")
    for beer in beers:
        values = [
            getattr(beer, header).strftime("%Y-%M-%d")
            if header == "date"
            else str(getattr(beer, header))
            for header in headers
        ]
        table.add_row(*values)
    console.print(table)
