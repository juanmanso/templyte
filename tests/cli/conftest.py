import click.testing
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


mock_response = {
    "title": "Lorem Ipsum",
    "extract": "Lorem ipsum dolor sit amet",
}

""" Setting up tests with fixtures """


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = mock_response
    return mock


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("cli.wikipedia.random_page")
