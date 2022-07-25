"""Beerlog models representations."""

from datetime import datetime
from statistics import mean
from typing import Dict, Optional

from pydantic import validator
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Beer(SQLModel, table=True):
    """Beer model representation."""

    __table_args__ = (UniqueConstraint("name", "style"),)

    id_: Optional[int] = Field(primary_key=True, default=None, index=True)
    # TODO add constraint in str/int size
    name: str
    style: str
    flavor: int
    image: int
    cost: int
    rate: int = 0
    date: datetime = Field(default_factory=datetime.now)

    # pylint: disable=no-self-argument
    @validator("flavor", "image", "cost")
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
        RuntimeError
            If user input was invalid.

        """
        if value < 1 or value > 10:
            # ValueError do not stop validator with always=True being called
            raise ArithmeticError(
                f"\N{no entry} {field.name} must be between 1 and 10"
            )
        return value

    # pylint: disable=no-self-argument, unused-argument
    @validator("rate", always=True)
    def calculate_rate(
        cls, value: int, values: Dict[str, int]  # noqa: N805
    ) -> int:
        """
        Calculate rate for beer.

        Parameters
        ----------
        value : int
            Value stored.
        values : Dict[str, int]
            Values of the other fields.

        Returns
        -------
        int
            Beer rate.

        """
        rate = mean([values["flavor"], values["image"], values["cost"]])
        return int(rate)
