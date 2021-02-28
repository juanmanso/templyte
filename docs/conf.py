"""Sphinx configuration."""
from datetime import datetime

project = "Templyte"
author = "Juan Manso"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
html_static_path = ["_static"]
