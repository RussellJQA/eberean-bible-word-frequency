from datetime import date
from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako
import os
import zipfile

import requests  # pip install requests


def mkdir_if_not_isdir(folder):

    if not os.path.isdir(folder):
        os.mkdir(folder)


def get_binary_file_via_from_web(
    web_folder, binary_file, download_folder, force_download=False
):

    mkdir_if_not_isdir(download_folder)
    download_file = os.path.join(download_folder, binary_file)

    if force_download or not os.path.exists(download_file):

        binary_url = web_folder + binary_file
        resp = requests.get(binary_url)

        if resp.status_code == 200:
            with open(download_file, "wb") as write_file:
                write_file.write(resp.content)
        else:
            print(f"Download failed with status code: {resp.status_code}")


def unzip_data(download_folder, zip_fn, unzip_subfolder=None, check_files=None):

    unzip_path = (
        download_folder
        if unzip_subfolder is None
        else os.path.join(download_folder, unzip_subfolder)
    )
    mkdir_if_not_isdir(unzip_path)

    with zipfile.ZipFile(os.path.join(download_folder, zip_fn), "r") as zip_ref:

        if check_files is None:
            zip_ref.extractall(unzip_path)
        else:
            file_list = zip_ref.namelist()
            print(f"\nZip file {zip_fn} contains {len(file_list)} archived files.")

            desired_files = [file for file in file_list if check_files(file)]
            print(f"Unzipping the {len(desired_files)} desired files.")
            zip_ref.extractall(unzip_path, desired_files)


def get_base_template_args(description, keywords, title_h1):

    datestamp = date.today().strftime("%Y-%m-%d")

    base_template_args = {
        "description": "eBEREAN (electronic Bible Exploration REsources and ANalysis) - "
        + description,
        "keywords": keywords,
        "datestamp": datestamp,
        "author": "Russell Johnson",
        "site": "RussellJQA/eberean-bible-word-frequency",
        "year": datestamp[0:4],
        "og_site_name": "RussellJQA/eberean-bible-word-frequency",
        "title_h1": title_h1,
        "github_account": "https://github.com/RussellJQA",
    }

    return base_template_args


def write_html(base_template_args, new_template_args, mako_file, html_folder, html_fn):

    mkdir_if_not_isdir(html_folder)

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
