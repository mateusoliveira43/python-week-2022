"""Beerlog core functionalities."""

from typing import List, Optional

from sqlmodel import select

from beerlog.database import get_session
from beerlog.models import Beer


def add_beer_to_database(
    name: str,
    style: str,
    flavor: int,
    image: int,
    cost: int,
) -> bool:
    """
    Add a beer to service database.

    Parameters
    ----------
    name : str
        Beer's name.
    style : str
        Beer's style.
    flavor : int
        Beer's flavor.
    image : int
        Beer's image.
    cost : int
        Beer's cost.

    Returns
    -------
    bool
        True if operation was successfully; False otherwise.

    """
    with get_session() as session:
        beer = Beer(
            name=name, style=style, flavor=flavor, image=image, cost=cost
        )
        session.add(beer)
        session.commit()
    return True


def get_beers_from_database() -> List[Optional[Beer]]:
    """
    Get beers in service database.

    Returns
    -------
    List[Optional[Beer]]
        List of beers, if any.

    """
    with get_session() as session:
        sql = select(Beer)
        return list(session.exec(sql))  # type: ignore
