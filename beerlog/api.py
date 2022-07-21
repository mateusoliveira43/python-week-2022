"""Beerlog API."""

# Scripts that manipulate the shell must always be careful with possible
# security implications.
import subprocess  # nosec
from typing import List, Optional

from fastapi import FastAPI

from beerlog.core import get_beers_from_database
from beerlog.database import get_session
from beerlog.models import Beer
from beerlog.serializers import BeerIn, BeerOut

api = FastAPI(title="Beerlog")


@api.post("/beers/", response_model=BeerOut)
async def add_beers(beer_in: BeerIn) -> Beer:
    """
    Add a beer to service database.

    Parameters
    ----------
    beer_in : BeerIn
        Beer information.

    Returns
    -------
    Beer
        Beer added to database.

    """
    beer = Beer(**beer_in.dict())
    with get_session() as session:
        session.add(beer)
        session.commit()
        session.refresh(beer)
    return beer


@api.get("/beers/", response_model=List[Optional[BeerOut]])
async def list_beers() -> List[Optional[Beer]]:
    """
    List beers in service database.

    Returns
    -------
    List[Optional[Beer]]
        List of beers, if any.

    """
    beers = get_beers_from_database()
    return beers


def main() -> None:
    """Start Beerlog API."""
    command = "uvicorn beerlog.api:api --reload"
    try:
        subprocess.run(
            command, shell=True, check=True, encoding="utf-8"  # nosec
        )
    except KeyboardInterrupt:
        pass  # User stopped the service


if __name__ == "__main__":
    main()
