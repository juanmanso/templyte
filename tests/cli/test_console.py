import click.testing
import pytest
import requests

from cli import console
from conftest import mock_response

def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert mock_response["title"] in result.output

def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called

def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]

def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1

def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output

def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["--language=es"])
    mock_wikipedia_random_page.assert_called_with(language="es")

