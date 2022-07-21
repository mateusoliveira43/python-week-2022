"""Tests of the project serializers."""

from copy import deepcopy
from datetime import datetime

import pytest
from fastapi import HTTPException

from beerlog.serializers import BeerIn, BeerOut

FIELDS = ["flavor", "image", "cost"]
GOOD_RATINGS = [2, 3, 10]
BAD_RATINGS = [-5, 0, 12]
BEER_INFORMATION = {
    "name": "Beck's",
    "style": "Pilsen",
    "flavor": 1,
    "image": 1,
    "cost": 1,
}


def test_beer_in_model() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    assert BeerIn(**BEER_INFORMATION)


def test_beer_out_model() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    assert BeerOut(**BEER_INFORMATION, id_=1, rate=1, date=datetime.now())


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", GOOD_RATINGS)
def test_beer_in_model_validate_ratings(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(BEER_INFORMATION)
    beer_information[field] = rating
    beer = BeerIn(**beer_information)
    assert getattr(beer, field) == rating


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", BAD_RATINGS)
def test_beer_in_model_validate_ratings_error(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(BEER_INFORMATION)
    beer_information[field] = rating
    with pytest.raises(HTTPException) as error:
        BeerIn(**beer_information)
    assert field in str(error)
