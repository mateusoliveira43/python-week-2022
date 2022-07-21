"""API tests."""

from typing import Dict, List

from fastapi import status

from beerlog.models import Beer
from tests.conftest import DatabaseForTest


class TestAddRoute(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_add_beer(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.post(
            "/beers/",
            json={
                "name": "Skol",
                "style": "KornIPA",
                "flavor": 1,
                "image": 1,
                "cost": 2,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["name"] == "Skol"
        assert result["id_"] == 1


class TestListEmpty(DatabaseForTest):
    # noqa: D101 pylint: disable=missing-class-docstring

    def test_list_beers_empty(self) -> None:
        # noqa: D102 pylint: disable=missing-function-docstring
        response = self.test_api.get("/beers/")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 0


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
        response = self.test_api.get("/beers/")
        assert response.status_code == status.HTTP_200_OK
        result: List[Dict[str, str]] = response.json()
        assert len(result) == 2
        assert "Beck's" in result[0].values()
        assert "Brahma" in result[1].values()
