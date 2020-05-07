from datetime import date
from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako
import os


def get_base_template_args(description, keywords, title_h1):

    datestamp = date.today().strftime("%Y-%m-%d")

    base_template_args = {
        "description": "eBEREAN (electronic Bible Exploration REsources and ANalysis) - "
        + description,
        "keywords": keywords,
        "datestamp": datestamp,
        "author": "Russell Johnson",
        "site": "RussellJ.heliohost.org",
        "year": datestamp[0:4],
        "og_site_name": "RussellJ",
        "title_h1": title_h1,
    }

    return base_template_args


def write_html(base_template_args, new_template_args, mako_file, html_folder, html_fn):

    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)

    # Merge dictionaries
    filled_in_template_args = {**base_template_args, **new_template_args}
    # In Python 3.9, PEP 584 will let you merge  2 dicts using | or |=

    template_lookup = TemplateLookup([""])
    raw_template = Template(filename=mako_file, lookup=template_lookup)
    filled_in_template = raw_template.render(**filled_in_template_args)

    with open(
        os.path.join(html_folder, html_fn), "w", encoding="utf-8", newline=""
    ) as write_file:
        write_file.write(filled_in_template)
