import csv
import os
import re

from get_bible_data import get_bible_books, get_book_nums, get_verse_counts
from utils import get_base_template_args, write_html

bible_books = get_bible_books()
bible_book_names = {
    bible_books[bible_book][0]: bible_book for bible_book in bible_books
}


def get_top_7_words(csv_path):

    """From the page's linked-to .csv file, get a list of its 7 words with the
    highest weightedRelFreq (the .csv's first 7 words)
    """

    top_7_words = []
    with open(csv_path, mode="r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for count, row in enumerate(reader, start=-1):
            if count >= 1:  # We don't care about the 1st 2 rows
                top_7_words.append(row[0])
            if count == 7:  # We only care about 7 rows of data
                break
    return top_7_words


def get_bible_chapter_text(book_num, book_abbrev, chapter):

    book_int = (int(book_num) + 1) if (int(book_num) <= 39) else (int(book_num) + 30)
    revised_book_num = str(book_int).zfill(3)
    chapter_num = chapter.zfill(3 if (book_abbrev == "Psa") else 2)
    chapter_file = (
        f"eng-kjv_{revised_book_num}_{book_abbrev.upper()}_{chapter_num}_read.txt"
    )
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    chapter_path = os.path.join(source_files, chapter_file)

    with open(chapter_path, "r", encoding="utf-8", newline="") as read_file:
        lines = read_file.readlines()

    lines2 = []

    for line in lines[2:]:

        # TODO: If this is Psalm chapter 119, then add:
        #   Hebrew letters before lines 1, 9, etc.
        #   Ending/beginning paragraph tags (</p> ... <p>) before lines 9, 17, etc.

        line = re.sub("(^.+)", "\n                \\1", line.strip())
        #   Indent only the Bible text's HTML SOURCE code by 16-spaces
        #   (4 spaces in from the enclosing <p> and </p>).

        line = line.replace("    ¶ ", "</p>\n            <p>\n                ")
        #   Replace text's paragraph markers with properly (un-)indented
        #   HTML paragraph ending/beginning paragraph tags (</p> ... <p>).

        lines2.append(line)

    bible_chapter_text = "                " + "".join(lines2).strip()

    return bible_chapter_text


def write_bible_chapter(book_abbrev, chapter, words_in_chapter, rows):

    description = (
        f"KJV Bible Chapter Word Frequencies: {bible_book_names[book_abbrev]} {chapter}"
    )

    keywords = [
        "KJV",
        "Bible",
        bible_book_names[book_abbrev],
        f"{bible_book_names[book_abbrev]} {chapter}",
        "chapter",
        "word frequency",
    ]

    book_num = f"{str(get_book_nums()[book_abbrev]).zfill(2)}"
    html_folder = os.path.join(
        os.getcwd(), "public_html", f"{book_num}-{book_abbrev.lower()}"
    )
    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)
    csv_file_name = f"{book_abbrev.lower()}{str(chapter).zfill(3)}-word-freq.csv"
    keywords += get_top_7_words(os.path.join(html_folder, csv_file_name))
    # Include top 7 words in the page's keywords metatag

    base_template_args = get_base_template_args(
        description, ",".join(keywords), description
    )

    bible_chapter_text = get_bible_chapter_text(book_num, book_abbrev, chapter)

    new_template_args = {
        "resources_path": "..",
        "bible_book_name": bible_book_names[book_abbrev],
        "book_abbrev": book_abbrev,
        "chapters_in_book": get_verse_counts()[f"{book_abbrev} {chapter}"],
        "chapter": chapter,
        "words_in_bible": "790,663",
        "words_in_chapter": words_in_chapter,
        "csv_file_name": csv_file_name,
        "bible_chapter_text": bible_chapter_text,
        "rows": rows,
    }

    write_html(
        base_template_args,
        new_template_args,
        "bible_chapter.mako",
        html_folder,
        f"{book_abbrev.lower()}{chapter.zfill(3)}-word-freq.html",
    )


def main():

    book_abbrev = "Gen"
    chapter = "1"
    words_in_chapter = "797"
    rows = [
        ["whales", "1", "1", "992.0", "790,663"],
        ["yielding", "5", "7", "708.6", "564,759"],
    ]

    write_bible_chapter(book_abbrev, chapter, words_in_chapter, rows)


if __name__ == "__main__":
    main()
