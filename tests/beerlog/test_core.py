"""Test of project's core functionalities."""

from unittest.mock import Mock, patch

from beerlog.core import add_beer_to_database, get_beers_from_database
from beerlog.models import Beer
from tests import DatabaseForTest


class TestAdd(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    # TODO remove mocks, add responsibility to class
    @patch("beerlog.core.get_session")
    def test_add(self, mock_get_session: Mock) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        mock_get_session.return_value = self.session
        response = add_beer_to_database(
            name="Patagonia", style="IPA", flavor=8, image=6, cost=4
        )
        assert response is True

    # @patch("beerlog.core.get_session")
    # def test_add_error(self, mock_get_session: Mock) -> None:
    # TODO add database constraint: name + style must be unique


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    @patch("beerlog.core.get_session")
    def test_list_empty(self, mock_get_session: Mock) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        mock_get_session.return_value = self.session
        beers = get_beers_from_database()
        assert len(beers) == 0


class TestListNotEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    @classmethod
    def setUpClass(cls) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        super().setUpClass()

        common_info = {
            "style": "Pilsen",
            "flavor": 1,
            "image": 1,
            "cost": 1,
        }

        cls.session.add(Beer(name="Beck's", **common_info))
        cls.session.add(Beer(name="Brahma", **common_info))
        cls.session.commit()

    @patch("beerlog.core.get_session")
    def test_list_not_empty(self, mock_get_session: Mock) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        mock_get_session.return_value = self.session
        beers = get_beers_from_database()
        assert len(beers) == 2
