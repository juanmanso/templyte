# Python versioning

To manage Python packaging and dependencies, we use
 [Poetry](https://python-poetry.org/). However, for Python versioning
 itself, we use [pyenv](https://github.com/pyenv/pyenv).

In this document, we will go through the proces of adding and setting up
 different versions of Python to our project.

## Downloading new versions of Python

To download a version of Python that isn't already available on your
 machine, run the following command (replacing `<python_version>` with the
 actual targeted version):

```bash
pyenv install <python_version>
```

Then, to make it available inside the repository, type:

```bash
cd <your_repo_path>
pyenv local <python_version>
```

Now, you can check that the version is correctly installed by running:

```bash
$ python --version
Python <python_version>
```

If you installed an older version (for instance, `3.4.1`), then run:

```bash
$ python3.4 --version
Python 3.4.1
```

## Giving support to older versions

If after playing around with older versions, you find that your program
 works with some of them, Poetry's config file should be updated.

To do that, we simply head to the `pyproject.toml` file and change this
 line:

```toml
[tool.poetry.dependencies]
python = "^<python_version"
```

By using the caret char (`^`), we state that our package (repo) will work
 _up to the next major release_ of that version. For instance, if we were
 to have this `pyproject.toml` file:

```toml
[tool.poetry.dependencies]
python = "^3.4"
```

it will mean that we guarantee the package works for any upgrade of 3.4 to 3.9 of Python, but not to future Python 4.0 or past Python 2.\*.
