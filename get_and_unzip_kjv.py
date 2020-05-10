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

from utils import unzip_data
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


def get_and_unzip_kjv():

    """
    If KJV .zip file not yet downloaded or user (when prompted) requests to download it:
        Download it
        Unzip it
    """

    download_folder = "downloads"
    if not os.path.isdir(download_folder):
        os.mkdir(download_folder)
    zip_fn = "eng-kjv_readaloud.zip"
    zip_path = os.path.join(download_folder, zip_fn)

    prompt = f"\nFile {zip_fn} already exists, do you want to download it anyway [y/n, default: y]?: "
    if (not os.path.exists(zip_path)) or ((input(prompt)).lower() == "y"):
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


def main():

    get_and_unzip_kjv()


if __name__ == "__main__":
    main()
