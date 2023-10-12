"""Configuration file for the Sphinx documentation builder."""
import os
import sys
from datetime import datetime

# Insert the parent directory into the path
sys.path.insert(0, os.path.abspath("../your_source_code"))

project = "your-package-name"
year = datetime.now().year
copyright = f"{year}"
author = "your-name"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_baseurl = "/docs/"
pygments_style = "sphinx"

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "show-inheritance": True,
}

extensions = [
    "myst_parser",
    "sphinx_click",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.mermaid",
]
