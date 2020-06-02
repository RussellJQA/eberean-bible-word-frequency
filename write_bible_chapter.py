import csv
import os
import re

from utils import get_base_template_args, write_html
from get_downloads import get_downloads
from get_bible_data import get_bible_books, get_book_nums, get_verse_counts
from reformat_psalm_119 import reformat_psalm_119

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


def get_bible_chapter_text(book_num, book_abbrev, chapter, custom_paragraphing=False):

    chapter_num = chapter.zfill(3)
    chapter_file = f"{book_num}_{book_abbrev.upper()}_{chapter_num}.txt"
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "data", "kjv_no_subtitles")
    chapter_path = os.path.join(source_files, chapter_file)

    with open(chapter_path, "r", encoding="utf-8", newline="") as read_file:
        lines = read_file.readlines()

    if custom_paragraphing and book_abbrev == "Psa" and chapter == "119":
        lines = reformat_psalm_119(lines)
        # if book_abbrev == "Psa" and chapter == "119":
        #     lines.append([
        #         "<pre style='font-family:Georgia,serif;'>",
        #         + reformat_psalm_119(lines),
        #         + "</pre>"]
        #     )

    html_lines = []

    for line in lines:

        line = re.sub("(^.+)", "\n                \\1", line.strip("\n"))
        #   Indent only the Bible text's HTML SOURCE code by 16-spaces
        #   (4 spaces in from the enclosing <p> and </p>).

        if not custom_paragraphing:
            line = line.replace("    ¶ ", "</p>\n            <p>\n                ")
            #   Replace text's paragraph markers with properly (un-)indented
            #   HTML paragraph ending/beginning paragraph tags (</p> ... <p>).

        html_lines.append(line)

    return (
        f'            {"" if custom_paragraphing else "<p>"}\n'
        + f'                {"".join(html_lines).strip()}\n'
        + f'            {"" if custom_paragraphing else "</p>"}'
    )


def write_bible_chapter(
    book_abbrev, chapter, words_in_chapter, rows, custom_paragraphing=False
):

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
    os.makedirs(html_folder, exist_ok=True)
    csv_file_name = f"{book_abbrev.lower()}{str(chapter).zfill(3)}-word-freq.csv"
    keywords += get_top_7_words(os.path.join(html_folder, csv_file_name))
    # Include top 7 words in the page's keywords metatag

    base_template_args = get_base_template_args(
        description, ",".join(keywords), description
    )

    bible_chapter_text = get_bible_chapter_text(
        book_num, book_abbrev, chapter, custom_paragraphing=custom_paragraphing,
    )

    new_template_args = {
        "images_path": "../images",
        "styles_path": "../styles",
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
        "templates/bible_chapter.mako",
        html_folder,
        f"{book_abbrev.lower()}{chapter.zfill(3)}-word-freq.html",
    )


def write_genesis_1():

    """ Write an abridged version of the HTML chapter file for Genesis 1
    """

    gen001_word_freq = """word,numInChap,numInKjv,simpleRelFreq,weightedRelFreq
TOTAL (Gen 1),797,790663
whales,1,1,790663,992.0
yielding,5,7,564759,712.6
"""
    chapter_folder = os.path.join(os.getcwd(), "public_html", "01-gen")
    os.makedirs(chapter_folder, exist_ok=True)

    with open(
        os.path.join(chapter_folder, "gen001-word-freq.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as write_file:
        write_file.write(gen001_word_freq)

    get_downloads()

    book_abbrev = "Gen"
    chapter = "1"
    words_in_chapter = "797"
    rows = [
        ["whales", "1", "1", "790,663", "992.0"],
        ["yielding", "5", "7", "564,759", "712.6"],
    ]

    write_bible_chapter(book_abbrev, chapter, words_in_chapter, rows)


def write_psalm_119():

    """ Write an abridged version of the HTML chapter file for Psalm 119
    """

    gen001_word_freq = """word,numInChap,numInKjv,simpleRelFreq,weightedRelFreq
TOTAL (Psa 119),2423,790663
forged,1,1,790663,326.3
grease,1,1,790663,326.3
"""
    chapter_folder = os.path.join(os.getcwd(), "public_html", "01-gen")
    os.makedirs(chapter_folder, exist_ok=True)

    with open(
        os.path.join(chapter_folder, "psa119-word-freq.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as write_file:
        write_file.write(gen001_word_freq)

    get_downloads()

    book_abbrev = "Psa"
    chapter = "119"
    words_in_chapter = "797"
    rows = [
        ["forged", "1", "1", "790,663", "326.3"],
        ["grease", "1", "1", "790,663", "326.3"],
    ]

    write_bible_chapter(
        book_abbrev, chapter, words_in_chapter, rows, custom_paragraphing=True
    )


def main():

    write_genesis_1()
    write_psalm_119()


if __name__ == "__main__":
    main()
