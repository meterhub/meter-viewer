# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from meterviewer import __version__

project = "Meter Viewer"
copyright = "2024, svtter"
author = "svtter"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "sphinx.ext.viewcode",
  "sphinx.ext.githubpages",
  "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autosummary_generate = True
add_module_names = False

language = "zh_CN"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# GitHub repository configuration
html_theme_options = {
    "github_url": "https://github.com/meterhub/meter-viewer",
    "style_external_links": True,
    "navigation_depth": 4,
}

# Project URLs
project_urls = {
    "GitHub": "https://github.com/meterhub/meter-viewer",
    "Issues": "https://github.com/meterhub/meter-viewer/issues",
}

source_suffix = [".rst"]
