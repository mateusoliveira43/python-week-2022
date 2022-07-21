"""Beerlog serializers."""

from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module


class BeerOut(BaseModel):
    # pylint: disable=too-few-public-methods
    """Beer model representation for endpoints responses."""

    id_: int
    name: str
    style: str
    flavor: int
    image: int
    cost: int
    rate: int
    date: datetime


class BeerIn(BaseModel):
    # pylint: disable=too-few-public-methods
    """Beer information for post endpoints."""

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
        HTTPException
            If user input was invalid.

        """
        if value < 1 or value > 10:
            raise HTTPException(
                detail=f"{field.name} must be between 1 and 10",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return value
