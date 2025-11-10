import sys
from pathlib import Path

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "dicechanics"
copyright = "2025, Daniel Ploug Hall"
author = "Daniel Ploug Hall"
release = "2.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = []
exclude_trees = [".venv"]

sys.path.insert(0, str(Path("..\\..", ".").resolve()))
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"
