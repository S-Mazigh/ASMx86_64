# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ASMx86_64'
copyright = '2024-2025'
author = 's-mazigh'
release = '0.25.12'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add sphinx-book-theme to extensions
extensions = [
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx_book_theme',
    'sphinx_togglebutton',
    'sphinx_subfigure',
    'sphinx_design'
]

myst_enable_extensions = [
    # "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    # "fieldlist",
    # "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    # "substitution",
    "tasklist",
]

# Améliorer la recherche
html_search_language = 'fr'

# Ajouter un footer avec dernière mise à jour
html_last_updated_fmt = '%d/%m/%Y'

# Numérotation automatique des figures
numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Tableau %s',
    'code-block': 'Listing %s'
}

# Index plus détaillé
html_domain_indices = True

# In order for sphinx to generate refs for headers up to level 3
myst_heading_anchors = 3

# find a way to template the slides instead of having the full header in each file
templates_path = ['_templates']
    
exclude_patterns = ["drafts/*"]

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Set the theme
html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_css_files = [
    'css/mystyle.css',
]

# Configure the theme
html_theme_options = {
    "repository_url": "https://github.com/S-Mazigh/ASMx86_64",  # Optional: your GitHub repository URL
    "use_repository_button": True,      # Optional: adds a link to your repository
    "use_issues_button": True,          # Optional: adds a link to your repository's issues
    # "use_edit_page_button": True,       # Optional: adds an edit button to pages
    # "path_to_docs": "docs",             # Optional: path to your docs relative to repository root
    "show_navbar_depth": 2,             # Controls depth of navigation in sidebar
}

# Other useful configurations
html_title = "ASMx86_64"
html_logo = "_static/athlon.png"  # Optional: path to your logo
html_favicon = "_static/athlon.png"  # Optional: path to your logo
