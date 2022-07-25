"""Tests of the project serializers."""

from copy import deepcopy

import pytest

from beerlog.serializers import BeerIn, BeerOut
from tests.conftest import PATAGONIA

FIELDS = ["flavor", "image", "cost"]
GOOD_RATINGS = [4, 7, 9]
BAD_RATINGS = [-10, -1, 11]


def test_beer_in_model() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    assert BeerIn(**PATAGONIA)


def test_beer_out_model() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    assert BeerOut(**PATAGONIA, id_=1, rate=1, date="15/02/2006")


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", GOOD_RATINGS)
def test_beer_in_model_validate_ratings(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(PATAGONIA)
    beer_information[field] = rating
    beer = BeerIn(**beer_information)
    assert getattr(beer, field) == rating


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", BAD_RATINGS)
def test_beer_in_model_validate_ratings_error(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(PATAGONIA)
    beer_information[field] = rating
    with pytest.raises(ValueError) as error:
        BeerIn(**beer_information)
    assert field in str(error)
