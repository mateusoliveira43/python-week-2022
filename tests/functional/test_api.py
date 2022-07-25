"""API tests."""

from fastapi import status
from fastapi.testclient import TestClient

from beerlog.api.__main__ import api
from beerlog.models import Beer
from tests.conftest import (
    BEER_COMMON_INFO,
    HEINEKEN,
    PATAGONIA,
    DatabaseForTest,
)

BEER_ENDPOINT = "/beers/"


def test_docs() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    response = TestClient(api).get("/")
    assert response.status_code == status.HTTP_200_OK


def test_redoc() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    response = TestClient(api).get("/redoc")
    assert response.status_code == status.HTTP_200_OK


class TestAddRoute(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_add_beer(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.post(
            BEER_ENDPOINT,
            data=PATAGONIA,
        )
        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["was_successful"] is True
        assert "beer added" in result["message"]
        assert len(result["beers"]) == 1


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_list_beers_empty(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.get(BEER_ENDPOINT)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        result = response.json()
        assert "no beer" in result["detail"]


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
        response = self.test_api.get(BEER_ENDPOINT)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["was_successful"] is True
        assert "3 beer(s)" in result["message"]
        assert len(result["beers"]) == 3

    def test_list_beers_with_style(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.get(f"{BEER_ENDPOINT}?style=Pilsen")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["was_successful"] is True
        assert "2 beer(s)" in result["message"]
        assert len(result["beers"]) == 2

    def test_list_beers_empty_with_style(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.get(f"{BEER_ENDPOINT}?style=IPA")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        result = response.json()
        assert "No beer" in result["detail"]
