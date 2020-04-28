from datetime import date
import os

# pip-installed
from mako.template import Template
from mako.lookup import TemplateLookup

template_lookup = TemplateLookup([""])
raw_template = Template(
    filename="bible_book_index_template.mako", lookup=template_lookup
)

# Data which varies between Bible books
book_abbrev = "Gen"
chapters_in_book = 50

# Data which is the same for each Bible book
description = "eBEREAN: electronic Bible Exploration REsources and ANalysis."
datestamp = date.today().strftime("%Y-%m-%d")
year = datestamp[0:4]
author = "Russell Johnson"
site = "RussellJ.heliohost.org"
title_h1 = f"{book_abbrev}: KJV Chapter Word Frequencies"
og_site_name = "RussellJ"

base_template_args = {
    "description": description,
    "datestamp": datestamp,
    "author": author,
    "site": site,
    "year": year,
    "og_site_name": og_site_name,
    "title_h1": title_h1,
}

new_template_args = {
    "book_abbrev": book_abbrev,
    "chapters_in_book": 50,
}

filled_in_template_args = {**base_template_args, **new_template_args}
# In Python 3.9, PEP 584 will let you add 2 dicts using | or |=
filled_in_template = raw_template.render(**filled_in_template_args)

html_folder = os.path.join(os.getcwd(), "NEW_HTML")
if not os.path.isdir(html_folder):
    os.mkdir(html_folder)

html_fn = "Gen_index.html"
with open(os.path.join(html_folder, html_fn), "w") as write_file:
    write_file.write(filled_in_template)
