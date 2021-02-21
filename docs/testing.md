# Testing

<!-- toc -->
- [Unit testing](#unit-testing)
- [Adding code coverage to pytest](#adding-code-coverage-to-pytest)
- [Automating tests with Nox](#automating-tests-with-nox)
<!-- end-toc -->

## Unit testing

Unit tests are the way to validate if a _portion of code_ has the functionality
it is supposed to. With them, we ensure that code is reliable and reusable.

There are several frameworks for testing. The most important ones are
[unittest](https://docs.python.org/3/library/unittest.html) and
[pytest](https://docs.pytest.org/en/latest/). We are going to use _pytest_
since [it is widely used](https://www.einfochips.com/blog/most-widely-used-python-based-test-automation-frameworks/).

Tests will be located into a separated folder from `src`, but following the
inner structure of `src`. For example, in our particular case:

```
.
├── src
│   └── cli
│       ├── __init__.py
│       └── console.py
└── tests
    ├── __init__.py
    └── cli
        └── test_console.py
```

The `__init__.py` is an empty file used to declare the test suite as a package.
There are other uses for that file, but for the scope of this sample, we are
going to leave it blank.

Naming convention for tests is straight forward: the filename will start with
the prefix `test_` and then end it with the name of the file to be tested.

The content of `test_console.py` will be the following:

```python
import click.testing
import pytest

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
```

The logic for the runner is extracted to a _test fixture_ because it will be
needed in most test cases inside the module. For instance, using the fixture on
a different test file on the same module will work, regardless if it is on one
file or the other. It is a good practice to extract them to a `conftest.py`
file for implicit import on test files/modules.
[PyTest's test fixtures](https://docs.pytest.org/en/latest/fixture.html) offer
explicit, modular and scalable initializations for test functions.

To run tests, we must invoke PyTest. Using Poetry we simply type:

```bash
poetry run pytest
```

## Adding code coverage to pytest

To do this, we simply install `coverge` and `pytest-cov` as dev dependencies.

Then, we need to tweak the `pyproject.toml` a bit to add `coverage` configs.
Most importantly, sources and minimum coverage threshold (set to 85\%).

With all set, we run `poetry run pytest --cov` and we should see the following
output:

```
================================ test session starts =================================
platform darwin -- Python 3.8.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/juanmanso/Documents/mine/templyte
plugins: cov-2.11.1
collected 1 item

tests/cli/test_console.py .                                                    [100%]

---------- coverage: platform darwin, python 3.8.2-final-0 -----------
Name                  Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------
src/cli/__init__.py       1      0      0      0   100%
src/cli/console.py       15      0      0      0   100%
-----------------------------------------------------------------
TOTAL                    16      0      0      0   100%

Required test coverage of 85.0% reached. Total coverage: 100.00%

================================= 1 passed in 2.73s =================================
```

## Automating tests with Nox

[Nox](https://nox.thea.codes/) is a package related to
[tox](https://tox.readthedocs.io/), useful for automating testing in multiple
versions of Python in isolated environments. To configure Nox, we create a
`noxfile.py` as shown below.

```python
# noxfile.py
import nox


@nox.session(python=["3.8", "3.7"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
```

In there, we define a session (`tests`) that install dependencies and run the
actual test suite. Since Poetry is not part of the environment created by Nox,
we need to flag it as `external`.

On each invocation of Nox, it recreates the environments from scrach, but if we
add the `-r` flag, it will reuse the existing ones.

Lastly, the `session.posargs` associated with the variable `args`, enables
receiving command line arguments to alter the `pytest` command. As a default,
we leave the `--cov` argument, but it can be overwritten by doing:

```
nox -- tests/cli/test_console.py
```

This command will run the console tests but it will not print the coverage.
