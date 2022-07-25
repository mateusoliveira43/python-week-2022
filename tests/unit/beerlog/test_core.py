"""Test of project's core functionalities."""

from beerlog.core import add_beer_to_database, get_beers_from_database
from beerlog.models import Beer
from beerlog.serializers import OperationFinished
from tests.conftest import (
    BEER_COMMON_INFO,
    COFFEE,
    HEINEKEN,
    PATAGONIA,
    DatabaseForTest,
)


class TestAdd(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    result_success: OperationFinished
    result_duplication: OperationFinished
    result_validation_error: OperationFinished

    @classmethod
    def setUpClass(cls) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        super().setUpClass()

        cls.result_success = add_beer_to_database(**PATAGONIA)  # type: ignore
        cls.result_duplication = add_beer_to_database(
            **PATAGONIA  # type: ignore
        )
        cls.result_validation_error = add_beer_to_database(
            **COFFEE  # type: ignore
        )

    def test_add_success_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_success.was_successful is True

    def test_add_success_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert "beer added to database" in self.result_success.message

    def test_add_success_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_success.beers) == 1

    def test_add_duplication_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_duplication.was_successful is False

    def test_add_duplication_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert (
            "beer with the same name and style"
            in self.result_duplication.message
        )

    def test_add_duplication_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_duplication.beers) == 0

    def test_add_validation_error_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_validation_error.was_successful is False

    def test_add_validation_error_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert (
            "must be between 1 and 10" in self.result_validation_error.message
        )

    def test_add_validation_error_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_validation_error.beers) == 0


class TestList(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    result_not_empty_without_style: OperationFinished
    result_not_empty_with_style: OperationFinished
    result_empty_with_style: OperationFinished

    @classmethod
    def setUpClass(cls) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        super().setUpClass()

        cls.session.add(Beer(name="Beck's", **BEER_COMMON_INFO))
        cls.session.add(Beer(name="Brahma", **BEER_COMMON_INFO))
        cls.session.add(Beer(**HEINEKEN))
        cls.session.commit()

        cls.result_not_empty_without_style = get_beers_from_database()
        cls.result_not_empty_with_style = get_beers_from_database(
            style="Pilsen"
        )
        cls.result_empty_with_style = get_beers_from_database(style="IPA")

    def test_list_not_empty_without_style_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_not_empty_without_style.was_successful is True

    def test_list_not_empty_without_style_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert "3 beer(s)" in self.result_not_empty_without_style.message

    def test_list_not_empty_without_style_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_not_empty_without_style.beers) == 3

    def test_list_not_empty_with_style_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_not_empty_with_style.was_successful is True

    def test_list_not_empty_with_style_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert "2 beer(s)" in self.result_not_empty_with_style.message

    def test_list_not_empty_with_style_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_not_empty_with_style.beers) == 2

    def test_list_empty_with_style_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result_empty_with_style.was_successful is False

    def test_list_empty_with_style_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert "No beer" in self.result_empty_with_style.message

    def test_list_empty_with_style_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result_empty_with_style.beers) == 0


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    result: OperationFinished

    @classmethod
    def setUpClass(cls) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        super().setUpClass()

        cls.result = get_beers_from_database()

    def test_list_empty_without_style_was_successful(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert self.result.was_successful is False

    def test_list_empty_without_style_message(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert "no beer" in self.result.message

    def test_list_empty_without_style_beers(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        assert len(self.result.beers) == 0
