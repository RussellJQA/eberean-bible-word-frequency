""" From https://ebible.org/Scriptures/eng-kjv_readaloud.zip/copr.htm:

...


King James Version + Apocrypha
The King James Version or Authorized Version of the Holy Bible, using the standardized text of 1769, with Apocrypha/Deuterocanon
[Public Domain](http://en.wikipedia.org/wiki/Public_domain)
Language: [English](http://www.ethnologue.org/language/eng)
Dialect: archaic British

Letters patent issued by King James with no expiration date means that to print this translation in the United Kingdom or import printed copies into the UK,
you need permission.
Currently, the Cambridge University Press, the Oxford University Press, and Collins have the exclusive right to print this Bible
translation in the UK. This royal decree has no effect outside of the UK, where this work is firmly in the Public Domain.
Please see http://www.cambridge.org/about-us/who-we-are/queens-printers-patent and https://en.wikipedia.org/wiki/King_James_Version#Copyright_status
for more information.
This free text of the King James Version of the Holy Bible is brought to you courtesy of the
[Crosswire Bible Society](https://crosswire.org/) and [eBible.org](https://ebible.org/).


2018-08-27

...

You may copy the King James Version of the Holy Bible freely. If you find a typo that is not just an archaic spelling,
[please report it](http://ebible.org/cgi-bin/comment.cgi).

...

"""

import os
import re
from shutil import copyfile

from utils import mkdir_if_not_isdir, unzip_data
from get_bible_data import get_binary_file_via_from_web


def is_desired_kjv_file(filename):

    apocryphal_pattern1 = "eng-kjv_04[123456789]_[3A-Z]{3,3}_[0-9]{2,2}_read.txt"
    match1 = re.search(apocryphal_pattern1, filename)

    apocryphal_pattern2 = "eng-kjv_05[0123456789]_[12A-Z]{3,3}_[0-9]{2,2}_read.txt"
    match2 = re.search(apocryphal_pattern2, filename)

    # keys.asc (PGP keys) or signature.txt.asc (PGP signed message)
    pgp_pattern = ".+.asc"
    match3 = re.search(pgp_pattern, filename)

    return not (match1 or match2 or match3)


def get_kjv():

    """
    If KJV .zip file not yet downloaded or user (when prompted) requests to download it:
        Download it
        Unzip it
    """

    download_folder = "downloads"
    mkdir_if_not_isdir(download_folder)
    zip_fn = "eng-kjv_readaloud.zip"
    zip_path = os.path.join(download_folder, zip_fn)

    prompt = (
        f"\nFile {zip_fn} already exists, do you want to download it anyway [y/N]?: "
    )
    if (not os.path.exists(zip_path)) or ((input(prompt)).lower() == "n"):
        get_binary_file_via_from_web(
            "https://ebible.org/Scriptures/",
            zip_fn,
            download_folder,
            force_download=True,
        )
        unzip_data(
            "downloads",
            "eng-kjv_readaloud.zip",
            "kjv_chapter_files",
            is_desired_kjv_file,
        )
        # Un-zipping un-zips 1191 files:
        #   1,189 KJV Bible chapter files
        #   copr.htm                        copyright info (as extracted from above)
        #   eng-kjv_000_000_000_read.txt    a README.txt file


def get_github_mark(html_folder):

    github_mark_path = "downloads/GitHub-Mark/PNG/GitHub-Mark-64px.png"
    if not os.path.exists(github_mark_path):
        get_binary_file_via_from_web(
            "https://github-media-downloads.s3.amazonaws.com/",
            "GitHub-Mark.zip",
            "downloads",
        )
        unzip_data("downloads", "GitHub-Mark.zip")

    mkdir_if_not_isdir(html_folder)
    images_folder = os.path.join(html_folder, "images")
    mkdir_if_not_isdir(images_folder)
    copyfile(
        github_mark_path, os.path.join(images_folder, "github-mark-64px.png"),
    )


# def get_sorttable_js(html_folder):

#     sorttable_js_path = "downloads/sorttable.js"
#     if not os.path.exists(sorttable_js_path):
#         get_binary_file_via_from_web(
#             "https://www.kryogenix.org/code/browser/sorttable/",
#             "sorttable.js",
#             "downloads",
#         )

#     mkdir_if_not_isdir(html_folder)
#     scripts_folder = os.path.join(html_folder, "scripts")
#     mkdir_if_not_isdir(scripts_folder)
#     copyfile(sorttable_js_path, os.path.join(scripts_folder, "sorttable.js"))


def get_downloads():

    get_kjv()
    html_folder = os.path.join(os.getcwd(), "public_html")
    get_github_mark(html_folder)

    # get_sorttable_js(html_folder)
    #   Skip this for now, and possibly permanently,
    #   so that I can use a modified version with a stable sort.


def main():

    get_downloads()


if __name__ == "__main__":
    main()
