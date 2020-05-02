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
import zipfile

from get_bible_data import get_binary_file_via_from_web


def get_zip_data(web_folder, zip_fn, download_folder):

    zip_downloaded = True

    if not os.path.isdir(download_folder):
        os.mkdir(download_folder)

    zip_path = os.path.join(download_folder, zip_fn)
    if os.path.exists(zip_path):
        response = input(
            f"\nFile {zip_fn} already exists, do you want to download it anyway [y/n, default: y]?: "
        ).lower()
        if response != "y":
            zip_downloaded = False
            return zip_downloaded
    get_binary_file_via_from_web(web_folder, zip_fn, download_folder, re_download=True)

    return zip_downloaded


def is_desired_file(filename):

    apocryphal_pattern1 = "eng-kjv_04[123456789]_[3A-Z]{3,3}_[0-9]{2,2}_read.txt"
    match1 = re.search(apocryphal_pattern1, filename)

    apocryphal_pattern2 = "eng-kjv_05[0123456789]_[12A-Z]{3,3}_[0-9]{2,2}_read.txt"
    match2 = re.search(apocryphal_pattern2, filename)

    # keys.asc (PGP keys) or signature.txt.asc (PGP signed message)
    pgp_pattern = ".+.asc"
    match3 = re.search(pgp_pattern, filename)

    return not (match1 or match2 or match3)


def unzip_data(download_folder, zip_fn, unzip_subfolder):

    unzip_path = os.path.join(download_folder, unzip_subfolder)
    if not os.path.isdir(unzip_path):
        os.mkdir(unzip_path)

    with zipfile.ZipFile(os.path.join(download_folder, zip_fn), "r") as zip_ref:

        file_list = zip_ref.namelist()
        print(f"\nZip file {zip_fn} contains {len(file_list)} archived files.")

        desired_files = [file for file in file_list if is_desired_file(file)]
        print(f"Unzipping the {len(desired_files)} desired files.")
        zip_ref.extractall(unzip_path, desired_files)


def get_and_unzip_kjv():

    """
    If a new .zip file is downloaded, then un-zip it
    """

    # .zip file linked to at https://ebible.org/kjv/
    if get_zip_data(
        r"https://ebible.org/Scriptures/", "eng-kjv_readaloud.zip", "downloads"
    ):
        unzip_data("downloads", "eng-kjv_readaloud.zip", "kjv_chapter_files")

    # Un-zipping un-zips 1191 files:
    #   1,189 KJV Bible chapter files
    #   copr.htm                        copyright info (as extracted from above)
    #   eng-kjv_000_000_000_read.txt    a README.txt file


def main():

    get_and_unzip_kjv()


if __name__ == "__main__":
    main()
