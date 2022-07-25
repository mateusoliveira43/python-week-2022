"""Beerlog core functionalities."""

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from beerlog.database import get_session
from beerlog.models import Beer
from beerlog.serializers import (
    BeerIn,
    OperationFinished,
    serialize_beer_model_for_output,
)


def add_beer_to_database(
    name: str,
    style: str,
    flavor: int,
    image: int,
    cost: int,
) -> OperationFinished:
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
    OperationFinished
        Information about the operation.

    """
    try:
        beer_input = BeerIn(
            name=name, style=style, flavor=flavor, image=image, cost=cost
        )
        with get_session() as session:
            beer = Beer(**beer_input.dict())
            session.add(beer)
            session.commit()
            session.refresh(beer)
        return OperationFinished(
            was_successful=True,
            message="\N{beer mug} beer added to database",
            beers=[serialize_beer_model_for_output(beer)],
        )
    except ValueError as error:
        return OperationFinished(
            was_successful=False, message=str(error), beers=[]
        )
    except IntegrityError:
        return OperationFinished(
            was_successful=False,
            message=(
                "\N{no entry} beer with the same name and style "
                "already exists"
            ),
            beers=[],
        )


def get_beers_from_database(
    style: Optional[str] = None,
) -> OperationFinished:
    """
    Get beers in service database.

    Parameters
    ----------
    style : Optional[str]
        Filter of beer's style to be applied, by default None.

    Returns
    -------
    OperationFinished
        Information about the operation.

    """
    with get_session() as session:
        sql = select(Beer)
        if style:
            sql = sql.where(Beer.style == style)
        beers = list(session.exec(sql))
        len_beers = len(beers)
        if len_beers == 0:
            return OperationFinished(
                was_successful=False,
                message=(
                    f"\N{cross mark} No beer of the style {style} stored yet"
                    if style
                    else "\N{cross mark} There is no beer stored yet"
                ),
                beers=[],
            )
        return OperationFinished(
            was_successful=True,
            message=f"\N{clinking beer mugs} {len_beers} beer(s) retrieved!",
            beers=[serialize_beer_model_for_output(beer) for beer in beers],
        )
