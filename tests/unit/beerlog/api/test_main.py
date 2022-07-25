"""Tests of main functionality."""

from unittest.mock import Mock, patch

from beerlog.api.__main__ import main


@patch("subprocess.run")
def test_main_stop(mock_subprocess: Mock) -> None:
    # noqa: D103 pylint: disable=missing-function-docstring
    mock_subprocess.side_effect = KeyboardInterrupt
    main()
    mock_subprocess.assert_called_once()
