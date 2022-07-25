"""Tests of the project models representation."""

from copy import deepcopy

import pytest

from beerlog.models import Beer
from tests.conftest import PATAGONIA

FIELDS = ["flavor", "image", "cost"]
GOOD_RATINGS = [2, 3, 10]
BAD_RATINGS = [-5, 0, 12]


def test_beer_model() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer = Beer(**PATAGONIA)
    assert "id_" in str(beer)
    assert "rate" in str(beer)
    assert "date" in str(beer)


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", GOOD_RATINGS)
def test_beer_model_validate_ratings(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(PATAGONIA)
    beer_information[field] = rating
    beer = Beer(**beer_information)
    assert getattr(beer, field) == rating


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("rating", BAD_RATINGS)
def test_beer_model_validate_ratings_error(field: str, rating: int) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer_information = deepcopy(PATAGONIA)
    beer_information[field] = rating
    with pytest.raises(ArithmeticError) as error:
        Beer(**beer_information)
    assert field in str(error)


def test_beer_model_calculate_rate() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    beer = Beer(**PATAGONIA)
    assert beer.rate == 6
