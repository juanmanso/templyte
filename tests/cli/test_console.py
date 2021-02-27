"""Test cases for the console module."""
from unittest.mock import Mock

from click.testing import CliRunner
from conftest import mock_response
import pytest
import requests

from cli import console


# TODO: replace mocks with fake api server


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It succeds, exiting with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints the title of the Wikipedia page."""
    result = runner.invoke(console.main)
    assert mock_response["title"] in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It invokes requests.get."""
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It uses the English Wikipedia by default."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """It uses the specified language edition of Wikipedia."""
    runner.invoke(console.main, ["--language=es"])
    mock_wikipedia_random_page.assert_called_with(language="es")


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exits with a non-zero status code if the request fails."""
    mock_requests_get.side_effect = Exception("Boom!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It prints an error message if the request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


@pytest.mark.e2e
def test_main_suceeds_in_production_env(runner: CliRunner) -> None:
    """It suceeds, exiting with a status code of zero (end-to-end)."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
