"""Tests configurations for the project."""

import functools
import inspect
import tempfile
from typing import Any, Callable, List, TypeVar
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.future import Engine
from sqlmodel import Session, create_engine
from typer.testing import CliRunner, Result  # type: ignore

from beerlog import models
from beerlog.api.__main__ import api
from beerlog.cli.__main__ import CLI

PATAGONIA = {
    "name": "Patagonia",
    "style": "IPA",
    "flavor": 8,
    "image": 6,
    "cost": 4,
}
COFFEE = {
    "name": "café",
    "style": "ruim",
    "flavor": -1,
    "image": -1,
    "cost": -1,
}
BEER_COMMON_INFO = {
    "style": "Pilsen",
    "flavor": 1,
    "image": 1,
    "cost": 1,
}
HEINEKEN = {
    "name": "Heineken",
    "style": "Larger",
    "flavor": 7,
    "image": 9,
    "cost": 1,
}


ReturnT = TypeVar("ReturnT")


class DatabaseForTest(TestCase):
    """Create database session for tests using unittest.TestCase."""

    engine: Engine
    session: Session
    test_api: TestClient
    test_cli: Callable[[Any, List[str]], Result]

    def __init_subclass__(cls) -> None:
        """Init class that inherits from DatabaseForTest."""
        cls.engine = create_engine(f"sqlite:///{tempfile.mkstemp()[1]}")
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, cls.override_database(method))
        for name, method in inspect.getmembers(cls, inspect.ismethod):
            setattr(cls, name, cls.override_database(method))

    @classmethod
    def override_database(
        cls, func: Callable[..., ReturnT]
    ) -> Callable[..., ReturnT]:
        """
        Override function to use test database.

        Parameters
        ----------
        func : Callable[..., ReturnT]
            Function to be override.

        Returns
        -------
        Callable[..., ReturnT]
            Overridden function.

        """

        @functools.wraps(func)
        def wrap(*args: Any, **kwargs: Any) -> ReturnT:
            with patch("beerlog.database.engine", cls.engine):
                return func(*args, **kwargs)

        return wrap

    def run_cli(self, arguments: List[str]) -> Result:
        """
        Run service CLI test client.

        Parameters
        ----------
        arguments : List[str]
            Arguments of the CLI.

        Returns
        -------
        Result
            Captured result of an invoked CLI script.

        """
        return CliRunner().invoke(CLI, arguments)

    @classmethod
    def setUpClass(cls) -> None:
        """Run before the class tests."""
        models.SQLModel.metadata.create_all(cls.engine)  # type: ignore
        cls.session = Session(cls.engine)
        cls.test_api = TestClient(api)
        cls.test_cli = cls.run_cli

    @classmethod
    def tearDownClass(cls) -> None:
        """Run after the class tests."""
        models.SQLModel.metadata.drop_all(cls.engine)  # type: ignore
