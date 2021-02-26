from unittest.mock import Mock

from _pytest.config import Config
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


mock_response = {
    "title": "Lorem Ipsum",
    "extract": "Lorem ipsum dolor sit amet",
}

""" Setting up tests with fixtures """


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = mock_response
    return mock


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    return mocker.patch("cli.wikipedia.random_page")
