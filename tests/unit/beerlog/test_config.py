"""Test Beerlog configurations."""

from unittest.mock import Mock, patch

from beerlog.config import get_database_engine


def test_config_sqlite() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    mock_settings = Mock()
    mock_settings.get.return_value = "FALSE"
    with patch("beerlog.config.settings", mock_settings):
        assert "sqlite" in get_database_engine()


def test_config_postgresql() -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    mock_settings = Mock()
    mock_settings.get.return_value = "TRUE"
    with patch("beerlog.config.settings", mock_settings):
        assert "postgresql" in get_database_engine()
