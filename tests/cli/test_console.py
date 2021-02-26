from unittest.mock import Mock

from click.testing import CliRunner
from conftest import mock_response
import pytest
import requests

from cli import console


# TODO: replace mocks with fake api server


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert mock_response["title"] in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, ["--language=es"])
    mock_wikipedia_random_page.assert_called_with(language="es")


@pytest.mark.e2e
def test_main_suceeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
