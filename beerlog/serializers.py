"""Beerlog serializers."""

from __future__ import annotations

from typing import List, Optional

from fastapi import Form
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module

from beerlog.models import Beer


class BeerIn(BaseModel):
    """Beer model serializer for input."""

    name: str
    style: str
    flavor: int
    image: int
    cost: int

    # pylint: disable=no-self-argument
    @validator("image", "flavor", "cost")
    def validate_ratings(
        cls, value: int, field: ModelField  # noqa: N805
    ) -> int:
        """
        Validate ratings for flavor, image and cost fields.

        Parameters
        ----------
        value : int
            Value user inserted.
        field : pydantic.fields.ModelField
            One of the fields to be validated.

        Returns
        -------
        int
            Validated value.

        Raises
        ------
        ValueError
            If user input was invalid: not between 1 and 10.

        """
        if value < 1 or value > 10:
            raise ValueError(
                f"\N{no entry} {field.name} must be between 1 and 10"
            )
        return value

    # pylint: disable=too-many-arguments
    @classmethod
    def form(
        cls,
        name: str = Form(...),
        style: str = Form(...),
        flavor: int = Form(...),
        image: int = Form(...),
        cost: int = Form(...),
    ) -> BeerIn:
        """
        Generate form for API endpoints.

        Parameters
        ----------
        name : str
            Beer's name, by default Form(...)
        style : str
            Beer's style, by default Form(...)
        flavor : int
            Beer's flavor, by default Form(...)
        image : int
            Beer's image, by default Form(...)
        cost : int
            Beer's cost, by default Form(...)

        Returns
        -------
        BeerIn
            Form for API endpoints.

        """
        return cls(
            name=name, style=style, flavor=flavor, image=image, cost=cost
        )


class BeerOut(BaseModel):
    # pylint: disable=too-few-public-methods
    """Beer model serializer for output."""

    id_: int
    name: str
    style: str
    flavor: int
    image: int
    cost: int
    rate: int
    date: str


class OperationFinished(BaseModel):
    # pylint: disable=too-few-public-methods
    """Finished database operation model serializer."""

    was_successful: bool
    message: str
    beers: List[Optional[BeerOut]]


def serialize_beer_model_for_output(beer: Beer) -> BeerOut:
    """
    Serialize beer model for user output.

    Parameters
    ----------
    beer : Beer
        Beer model.

    Returns
    -------
    BeerOut
        Serialized beer model for output.

    """
    return BeerOut(
        id_=beer.id_,
        name=beer.name,
        style=beer.style,
        flavor=beer.flavor,
        image=beer.image,
        cost=beer.cost,
        rate=beer.rate,
        date=beer.date.strftime("%d/%m/%Y"),
    )
