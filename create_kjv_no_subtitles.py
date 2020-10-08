import glob
import os
import re

from get_downloads import get_downloads


def create_kjv_no_subtitles():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    get_downloads()  # Download KJV chapter files, if needed

    bare_bones_kjv = os.path.join(script_dir, "data", "kjv_no_subtitles")
    os.makedirs(bare_bones_kjv, exist_ok=True)

    kjv_source = glob.glob(os.path.join(source_files, "*.txt"))
    for chapter_file in kjv_source:

        basename = os.path.basename(chapter_file)
        if basename != "eng-kjv_000_000_000_read.txt":
            #   Ignore what's essentially a README.txt file

            with open(chapter_file, "r", encoding="utf-8") as read_file:
                lines = read_file.readlines()

            pattern = r"eng-kjv_(\d{3})(_[1-3A-Z]{3}_)(\d{2,3})_read.txt"
            match = re.search(pattern, basename)
            if match:
                book_num = int(match.group(1))
                book_num = (book_num - 1) if (book_num <= 40) else (book_num -
                                                                    30)
                chapter_num = str(int(match.group(3))).zfill(3)
                basename = (f"{str(book_num).zfill(2)}"
                            f"{match.group(2)}{chapter_num}.txt")

            bare_bones_chapter_file = os.path.join(bare_bones_kjv, basename)
            with open(bare_bones_chapter_file, "w",
                      encoding="utf-8") as write_file:
                for line in lines[2:]:
                    line = re.sub("¶ ", "",
                                  line)  # Eliminate paragraph markers
                    write_file.writelines(
                        line.lstrip(" "))  # Eliminate leading blanks


def main():

    create_kjv_no_subtitles()


if __name__ == "__main__":
    main()
