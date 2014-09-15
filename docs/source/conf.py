#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '_themes'))

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

  # only import and set the theme if we're building docs locally
if not on_rtd:
    import alabaster
    html_theme = 'alabaster'
    html_theme_path = [alabaster.get_html_theme_path()]

extensions = ['alabaster']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'sliced'
copyright = '2014, Brian Peterson'
version = '0.1'
release = '0.1'

html_static_path = ['_static']
html_theme_options = {
    'logo': 'logo.png',
    'github_button': 'false',
    'github_user': 'bpeterso2000',
    'github_repo': 'sliced',
    'description': 'a Python slicing toolkit.',
}

html_title = 'sliced'
html_short_title = 'Python slice tools'
#html_logo = None
#html_favicon = None
html_sidebars = {'**': [
    'about.html', 'navigation.html', 'searchbox.html'
]}
htmlhelp_basename = 'sliceddoc'

exclude_patterns = ['_build']
pygments_style = 'sphinx'


latex_elements = {}
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'sliced.tex', 'sliced Documentation',
     'Brian Peterson', 'manual'),
]

man_pages = [
    ('index', 'sliced', 'sliced Documentation',
     ['Brian Peterson'], 1)
]

texinfo_documents = [
    ('index', 'sliced', 'Sliced',
     'Brian Peterson', 'sliced', 'Python slice tools.',
     'Miscellaneous'),
]
