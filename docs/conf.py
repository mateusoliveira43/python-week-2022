"""Configuration file for Sphinx."""

# -- Path setup --------------------------------------------------------------

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1].as_posix()

sys.path.append(PROJECT_ROOT)


# -- Project information -----------------------------------------------------

project = "Python project template"
copyright = "2022, Mateus Oliveira"
author = "Mateus Oliveira"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]
nitpick_ignore = [
    ("py:class", "datetime.datetime"),
    ("py:class", "sqlmodel.main.SQLModel"),
    ("py:class", "sqlmodel.orm.session.Session"),
    ("py:class", "pydantic.fields.ModelField"),
    ("py:class", "pydantic.main.BaseModel"),
    ("py:exc", "fastapi.HTTPException"),
]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
