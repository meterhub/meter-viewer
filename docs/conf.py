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


# GitHub 仓库地址
html_context = {
  "display_github": True,  # 是否显示 GitHub 链接（sphinx_rtd_theme 特有）
  "github_user": "meterhub",
  "github_repo": "meter-viewer",
  "github_version": "main",  # 分支名
  "conf_py_path": "/docs/",  # 文档所在路径（仓库里的相对路径）
}


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

source_suffix = [".rst"]
