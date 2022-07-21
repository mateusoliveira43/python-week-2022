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
from beerlog.api import api
from beerlog.cli import main

ReturnT = TypeVar("ReturnT")


class DatabaseForTest(TestCase):
    """Create database session for tests using unittest.TestCase."""

    engine: Engine
    session: Session
    test_api: TestClient
    test_cli: Callable[[Any, List[str]], Result]

    def __init_subclass__(cls) -> None:
        """Init class that inherits from DatabaseForTest."""
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith("test_"):
                setattr(cls, name, cls.override_database(method))

    @staticmethod
    def override_database(
        func: Callable[..., ReturnT]
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
        def wrap(self: DatabaseForTest, *args: Any, **kwargs: Any) -> ReturnT:
            with patch("beerlog.database.engine", self.engine):
                return func(self, *args, **kwargs)

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
        return CliRunner().invoke(main, arguments)

    @classmethod
    def setUpClass(cls) -> None:
        """Run before the class tests."""
        cls.engine = create_engine(f"sqlite:///{tempfile.mkstemp()[1]}")
        models.SQLModel.metadata.create_all(cls.engine)  # type: ignore
        cls.session = Session(cls.engine)
        cls.test_api = TestClient(api)
        cls.test_cli = cls.run_cli

    @classmethod
    def tearDownClass(cls) -> None:
        """Run after the class tests."""
        models.SQLModel.metadata.drop_all(cls.engine)  # type: ignore
