extensions = [
    "myst_parser",
    "sphinx.ext.autodoc"
]

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'dollarmath'
]
myst_heading_anchors = 2

project = 'ufpy'
# html_logo = "l.png"
html_favicon = 'favicon.ico'
html_theme = 'furo'

html_theme_options = {
    "source_repository": "https://github.com/honey-team/ufpy",
    "source_branch": "main",
    "source_directory": "docs/source",
    "repository_branch": "main"
}

html_static_path = ["_static"]
templates_path = ["_templates"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}