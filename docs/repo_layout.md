# Repository layout

This repository follows the _src layout_. The implementation is straight
 forward, just structure your repository like:

```bash
|- src
|  |_ packagename
|     |- __init__.py
|     |_ ...
|- tests
|  |_ ...
|_ ... setup_files
```
In short, packages are grouped into separated folders, but all under the
 `src` folder. Then, tests follow the same convention but the root folder
 is called `tests`. Finally, on your root folder, general configuration
 files are placed.

For more information on the _src layout_ and why you should use it, please
 refer to the following pages:

- [The structure, on ionel's codelog article named "Pacakging a python library"](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)
- [Stance (or discussion) on src/directory - Issue on `pypa/packaging.python.org`](https://github.com/pypa/packaging.python.org/issues/320)

