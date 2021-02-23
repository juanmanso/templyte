# Python Template Repository

## Requirements

For this project to work, we need to have the following installed:
- `bash`, `curl`, `git`and `python`
- `pyenv`, `poetry`, `nox` and `pre-commit` (which can be installed either with `curl` or `pip`)

As a bonus, it may come in handy to have `pip` installed.

To install the second option (assuming that the essentials are already
installed), you can copy-and-paste the following commands:

```
curl https://pyenv.run | bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
pip install --user --upgrade nox
pip install --user --upgrade pre-commit
```

## Getting started

### Setup your GPG keys

[GPG](https://gnupg.org/) (GNU Privacy Guard) is an implementation of the
[OpenPGP](https://www.openpgp.org/) (Pretty Good Privacy) protocol which
allows to sign and encrypt data or a communication channel. **In this case,
we use GPG keys to sign commits or tags on GitHub**.

> The idea is to generate a **pair of keys private/public** so we can sign
> with the private key (which each developer keeps safe) and associate the
> public key to our GitHub account to verify the signature.

For installation and setup, follow [this tutorial](https://gist.github.com/Beneboe/3183a8a9eb53439dbee07c90b344c77e).
