"""Tests of the project."""

from pathlib import Path
from unittest import TestCase

from sqlalchemy.future import Engine
from sqlmodel import Session, create_engine

from beerlog import models

TESTS_FOLDER = Path(__file__).resolve().parent
DATABASE_FOR_TESTS = TESTS_FOLDER / "test.db"


class DatabaseForTest(TestCase):
    """Create database session for tests using unittest.TestCase."""

    engine: Engine
    session: Session

    @classmethod
    def setUpClass(cls) -> None:
        """Run before the class tests."""
        cls.engine = create_engine(
            "sqlite:///:memory:", connect_args={"check_same_thread": False}
        )
        models.SQLModel.metadata.create_all(cls.engine)  # type: ignore
        cls.session = Session(cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """Run after the class tests."""
        models.SQLModel.metadata.drop_all(cls.engine)  # type: ignore
