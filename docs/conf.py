"""Sphinx configuration."""
from datetime import datetime

from recommonmark.transform import AutoStructify

project = "Templyte"
author = "Juan Manso"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
html_static_path = ["_static"]


def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            "enable_auto_toc_tree": True,
            # 'enable_math': False,
            # 'enable_inline_math': False,
            # 'enable_eval_rst': True,
        },
        True,
    )
    app.add_transform(AutoStructify)
