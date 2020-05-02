from datetime import date


def get_base_template_args(title_h1):

    datestamp = date.today().strftime("%Y-%m-%d")

    base_template_args = {
        "description": "eBEREAN: electronic Bible Exploration REsources and ANalysis.",
        "datestamp": datestamp,
        "author": "Russell Johnson",
        "site": "RussellJ.heliohost.org",
        "year": datestamp[0:4],
        "og_site_name": "RussellJ",
        "title_h1": title_h1,
    }

    return base_template_args
