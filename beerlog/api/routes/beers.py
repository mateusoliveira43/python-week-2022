"""Beerlog API beers route."""

from typing import Optional

from fastapi import APIRouter, Depends, status

from beerlog.api.utils import parse_result
from beerlog.core import add_beer_to_database, get_beers_from_database
from beerlog.serializers import BeerIn, OperationFinished

router = APIRouter(
    prefix="/beers",
)


@router.post(
    "/", response_model=OperationFinished, status_code=status.HTTP_201_CREATED
)
async def add_beers(
    beer_in: BeerIn = Depends(BeerIn.form),
) -> OperationFinished:
    """
    Add a beer to service database.

    Parameters
    ----------
    beer_in : BeerIn, optional
        Beer information, by default Depends(BeerIn.form)

    Returns
    -------
    OperationFinished
        Information about a database operation.

    """
    return parse_result(add_beer_to_database(**beer_in.dict()))


@router.get("/", response_model=OperationFinished)
async def list_beers(style: Optional[str] = None) -> OperationFinished:
    """
    List beers in service database.

    List all beers, if no style is passed, else, list all beers of the selected
    style.

    Parameters
    ----------
    style : Optional[str], optional
        Filter of beer's style to be applied, by default None

    Returns
    -------
    OperationFinished
        Information about a database operation.

    """
    return parse_result(get_beers_from_database(style=style))
