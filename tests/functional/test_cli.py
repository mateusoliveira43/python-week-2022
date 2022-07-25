"""CLI tests."""

from beerlog.models import Beer
from tests.conftest import BEER_COMMON_INFO, HEINEKEN, DatabaseForTest

ADD_BUDWEISER = [
    "add",
    "Budweiser",
    "Larger",
    "--flavor=1",
    "--image=2",
    "--cost=3",
]


class TestAddSuccess(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_add_beer(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(ADD_BUDWEISER)
        assert result.exit_code == 0
        assert "beer added" in result.stdout


class TestAddError(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_add_beer_error(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        self.test_cli(ADD_BUDWEISER)
        result = self.test_cli(ADD_BUDWEISER)
        assert result.exit_code == 1
        assert "beer with the same name and style" in result.stdout


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_list_beers_empty(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(["list"])
        assert result.exit_code == 1
        assert "no beer" in result.stdout


class TestList(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    @classmethod
    def setUpClass(cls) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        super().setUpClass()

        cls.session.add(Beer(name="Beck's", **BEER_COMMON_INFO))
        cls.session.add(Beer(name="Brahma", **BEER_COMMON_INFO))
        cls.session.add(Beer(**HEINEKEN))
        cls.session.commit()

    def test_list_beers_without_style(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(["list"])
        assert result.exit_code == 0
        assert "3 beer(s)" in result.stdout
        assert "Brahma" in result.stdout
        assert "Beck's" in result.stdout
        assert "Heineken" in result.stdout

    def test_list_beers_with_style(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(["list", "Pilsen"])
        assert result.exit_code == 0
        assert "2 beer(s)" in result.stdout
        assert "Brahma" in result.stdout
        assert "Beck's" in result.stdout
        assert "Heineken" not in result.stdout
