"""CLI tests."""

from beerlog.models import Beer
from tests.conftest import DatabaseForTest


class TestAdd(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_add_beer(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(
            [
                "add",
                "Budweiser",
                "Larger",
                "--flavor=1",
                "--image=2",
                "--cost=3",
            ]
        )
        assert result.exit_code == 0
        assert "beer added" in result.stdout
        assert result.stderr_bytes is None


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_list_beers_empty(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(
            [
                "list",
            ]
        )
        assert result.exit_code == 0
        assert "Beerlog" in result.stdout
        assert result.stderr_bytes is None


class TestList(DatabaseForTest):
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

    def test_list_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        result = self.test_cli(
            [
                "list",
            ]
        )
        assert result.exit_code == 0
        assert "Beerlog" in result.stdout
        assert "Brahma" in result.stdout
        assert "Beck's" in result.stdout
        assert result.stderr_bytes is None
