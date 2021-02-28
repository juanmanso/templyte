# Code analysis and pre-commit hooks

<!-- toc -->
- [Overview](#overview)
- [Linting tools](#linting-tools)
- [Code formatting](#code-formatting)
- [Security](#security)
- [Running everything together with Nox](#running-everything-together-with-nox)
- [Pre-commit and hooks](#pre-commit-and-hooks)
    - [Setting up pre-commit hooks](#setting-up-pre-commit-hooks)
    - [Gitlint for commit-msg hook](#gitlint-for-commit-msg-hook)
<!-- end-toc -->

## Overview

To ensure good software quality, we require for tools that verify that code is
following the established rules of quality. Also, since generally a team is
involved in the development instead of a single individual, it is required that
the team shares a common style to make code homogeneous. Besides styling, there
are several checks that can be done automatically that exceed testing and fit
into code analysis.

In this article, we are going to do a walk-through the setup of this repository
to help developers focus on the _what_ rather than the _how_.

## Linting tools

[Linters](https://en.wikipedia.org/wiki/Lint_(software)) are a static code
analysis tool used to check if code follows a list of rules. These rules may be
related to styling, other about security and others may be related to bug
detection.

It is called _static_ code analysis because it does not require the code to be
ran. Instead it runs on the source code looking for patterns that match the
criteria.

Since Python is a flexible language focused on simple and easy to write code
(3rd principle of [the Zen of Python -- PEP 20](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python)),
some liberties are taken that, if unchecked, may turn development into a
chaotic environment.

Luckily, the Python community as agreed on some standards documented on [PEP 7
-- Style Guide for Python code ](https://www.python.org/dev/peps/pep-0008/) by
the **P**ython **E**nhancement **P**roposal.
[Flake8](https://flake8.pycqa.org/en/latest/) is the go-to linter, since it
integrates many other linters as well as having multiple plugins that extend
its functionalities.

To setup Flake8, a configuration file by the name `.flake8` is used. For
instance, the current `.flake8` is as goes:

```dosini
[flake8]
select = B,B9,BLK,C,E,F,I,S,W
ignore = E203,E501,W503
per-file-ignores = tests/*:S101
application-import-names = cli, tests
import-order-style = google
max-complexity = 10
max-line-length = 88
```

In particular, we walk through the `select` property below:

- `B` and `B9` are there to enable _flake8-bugbear_ which helps finding bugs
and design problems.

- `BLK` enables _black_ warnings to be triggered on Flake8 (more on _black_
[here](#code-formatting).

- `C` selects violations reported by [mccabe](https://github.com/PyCQA/mccabe)
that relate to code complexity.

- `E` and `W` enable errors and warnings related to style conventions set in
PEP 8, detected by [pycodestyle](https://github.com/pycqa/pycodestyle)

- `F` are errors recognized by [pyflakes](https://github.com/PyCQA/pyflakes),
looking for invalid Python code in source files.

- `I` enables [flake8-import-order](https://github.com/PyCQA/flake8-import-order)
checks, sustained by PEP 8. This plugin however, does not fix issues
automatically and there is a need to do it by hand. Other tools that manage
automated import linting are [asottile's reorder-python-
imports](https://github.com/asottile/reorder_python_imports) and
[isort](https://timothycrosley.github.io/isort/) (with its companion
[flake8-isort](https://github.com/gforcada/flake8-isort)).

- `S` stands for _security_, provided by [bandit](https://github.com/PyCQA/bandit)
and enabled by [flake8-bandit](https://github.com/tylerwince/flake8-bandit).

## Code formatting

Have you ever worked with a teammate that lints with tabs and other with spaces,
making everything a mess and very tedious to maintain?

This, as well as other examples, are tackled by code formatters to keep a
consistent style. For Python, a very common code formatting tool is
[Black](https://github.com/psf/black) as previously introduced.

The thing that makes Black great (which may come as a course to others), is its
lack of configurability. It takes a leap of faith to trust in such a program,
but the reward is the peace of mind that formatting will be consistent across
not only the project, but all projects that incorporate Black.

For those who are not entirely sold on the idea of delegating this to Black,
please check the [documentation](https://black.readthedocs.io/en/stable/the_black_code_style.html)
that explains how the PEP 8 is applied.

## Security

As we have already seen in the [linting tools section](#linting-tools), we have
_bandit_ checking known issues that can be detected through static file checking.

However, there is more to it regarding security. For finding security
vulnerabilities **in dependencies**, we use [Safety](https://github.com/pyupio/safety).
This package goes through our dependencies (provided a `requirements.txt` file)
and compares it with its curated database of insecure packages.

Using Safety, we can detect third-party vulnerabilities easily, keeping our
project secure.

Nonetheless, we can still improve our security using tools such as
[python-afl](https://github.com/jwilk/python-afl). This tool implements an
[American Fuzzy Lop](https://lcamtuf.coredump.cx/afl/) that uses an fuzzer
looking for security vulnerabilities.

> NOTE: `python-afl` is not yet incorporated in this repo but it is planned to be

## Running everything together with Nox

We want to have access to the aforementioned tools to continuously check if
our code is healthy or not. For that, we used Nox which gives us reliable and
repeatable checks.

To run a Nox session (similar to a "command"), we type:

```bash
nox -rs <session_name>
```

For instance, if we want to run the linter but just for `python3.8` (remember
that Nox handles also multiple versions of Python!) we need to do:

```bash
nox -rs lint-3.8
```

Additionally, for bypass default configuration and give our own command line
arguments, we need to add first two hyphens (`--`):

```bash
nox -rs tests -- -m tests/cli/test_console.py
```

The default action for Nox if called without arguments (by simply typing `nox`
on the terminal) is set by the `nox.options.sessions` parameter. The current
configuration is:

```py
nox.options.sessions = "lint", "safety", "tests"
```

Lastly, to run our code formatting tool Black, we simply run:

```bash
nox -rs black
```

## Pre-commit and hooks

Everything is fine until someone pushes unformatted or untested code to the
remote repository and messes with others development, or even the production
stage! We have tools to avoid this behavior by continuously integrating code
prior to the actual merging of it to the stable branches.

However, these pipelines, that protect stable branches from bad code, usually
take a good amount of time to run. When they are done, they may fail because of
a trailing whitespace and that may be frustrating for developers that might have
already changed scope to another task and now how to go back and fix things.

Pre-commit hooks come to save the day and make things
[fail fast](https://en.wikipedia.org/wiki/Fail-fast). When the developer
commits new code, the pre-commit hook will run a sequence of scripts either
fixing things, or blocking their commitment.

Since pre-commit hooks apply to only the staged files, it can run super fast
(assuming that commits are [small and atomic](https://deepsource.io/blog/git-best-practices/))
assuring the developer that their code won't fail except for some more specific
cases. Also, it will provide quick feedback to them and thus apply a fix on the
spot, rather than 30 minutes after pipelines are done.

### Setting up pre-commit hooks

After [installing `pre-commit`](https://pre-commit.com/#install) on our
machine, we configure it through the `pre-commit-config.yaml`. In there, we
define the hooks we want to run which can be remote-defined or local. An
example YAML file, which looks for some formatting, runs Black, linter and
tests should look like this:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: local
    hooks:
    -   id: black
        name: black
        entry: poetry run black
        language: system
        types: [python]
    -   id: flake8
        name: flake8
        entry: poetry run flake8
        language: system
        types: [python]
    -   id: pytest
        name: pytest
        entry: poetry run pytest -m "not e2e"
        exclude: noxfile.py
        pass_filenames: false
        language: system
        types: [python]
```

Something worth mentioning is how we run pytest on the pre-commit stage. Since
pre-commit runs _all staged files_ into those hooks, some files that are not
supposed to be tested make our tests crash. This is the case of `noxfile.py`
which has the `.py` filetype but it is rather a configuration file. To avoid
running tests for it, we added it under the `exclude` property.

Another important thing is to set `pass_filenames: false` to [disable per file
checks](https://stackoverflow.com/a/57233175). In particular, we are interested
in this because we are setting a coverage floor to our code. If we were to run
tests separately, coverage may be reduced unfairly.

### Gitlint for commit-msg hook

Lastly, to keep the repo clean and consistent, we want to lint commit messages.
You may be thinking... really? Checking commit messages?

Well, there is actually value in consistent commit messages. For starters, it
helps to carry a methodology along the history of the repo and, if new devs
were to be on-boarded, they would have a better time reading through commits
and figure out what is going on and where.

Then, something interesting can happen if we guarantee consistent commit
messages: we can automate reports of the progress and status of our projects!

Take a look at [ohmyzsh](https://github.com/ohmyzsh/ohmyzsh). When updated, it
shows a beautiful changelog report.

![ohmyzsh changelog screenshot](https://res.cloudinary.com/practicaldev/image/fetch/s--KVroLuwO--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://dev-to-uploads.s3.amazonaws.com/i/hue3uxw462xm9o1yp7q7.png)

Well, the thing is that these reports are [based on the format of commit
messages](https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/changelog.sh)!
🤯

Now that we have understood the value of good formatted commit messages, let's
dive into the implementation. For linting these, we use
[gitlint](https://jorisroovers.com/gitlint/) which is a python library that
handles the burden for us.

Now, we simply add it with this code block:

```yaml
-   repo: https://github.com/jorisroovers/gitlint
    rev: v0.15.0
    hooks:
    -   id: gitlint
```

Since we are using Poetry to manage dependencies, we perform the check through
Poetry itself by doing:

```yaml
-   repo: local
    hooks:
    -   id: gitlint
        name: gitlint
        entry: poetry run gitlint -C gitlint/.gitlint --msg-filename .git/COMMIT_EDITMSG
        pass_filenames: false
        language: system
        always_run: true
        stages: [commit-msg]
```

As we can see above, we need to determine the rules for gitlint. This is done
on the `.gitlint` configuration file placed on the root which will be
automatically be picked by gitlint.

Finally, to actually add it to our pre-commit routine, we need first to
install the `commit-msg` hook since it is not installed by default (on
`pre-commit install`):

```bash
pre-commit install --hook-type commit-msg
```

<!-- TODO: Automate setup of pre-commit hooks -->
