# Setting up local dev environment

## MacOS 11 - Big Sur

At the time of the writing of this document, `pyenv` has [some issues](https://github.com/pyenv/pyenv/issues/1737) regarding the installation of python versions.

[The workaround](https://github.com/pyenv/pyenv/issues/1737#issuecomment-731672292) that worked on my machine for installing Python versions is shared below:

```diff
- pyenv install 3.8.2
+CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --patch 3.8.2 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```

More details will be shared on a follow-up series of commits, enhancing this documentation.
