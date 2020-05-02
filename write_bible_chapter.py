import os

from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako

from get_bible_data import get_bible_books, get_book_nums, get_verse_counts
from utils import get_base_template_args

template_lookup = TemplateLookup([""])
raw_template = Template(filename="bible_chapter_template.mako", lookup=template_lookup)

bible_books = get_bible_books()
bible_book_names = {
    bible_books[bible_book][0]: bible_book for bible_book in bible_books
}


def write_bible_chapter(book_abbrev, chapter, words_in_chapter, rows):

    verse_counts_by_chapter = get_verse_counts()

    base_template_args = get_base_template_args(
        f"{bible_book_names[book_abbrev]} {chapter}: Bible (KJV) Chapter Word Frequencies"
    )

    new_template_args = {
        "bible_book_name": bible_book_names[book_abbrev],
        "book_abbrev": book_abbrev,
        "chapters_in_book": verse_counts_by_chapter[f"{book_abbrev} {chapter}"],
        "chapter": chapter,
        "words_in_bible": "790,663",
        "words_in_chapter": words_in_chapter,
        "rows": rows,
    }

    # Merge dictionaries
    filled_in_template_args = {**base_template_args, **new_template_args}
    # In Python 3.9, PEP 584 will let you merge  2 dicts using | or |=
    filled_in_template = raw_template.render(**filled_in_template_args)

    book_nums = get_book_nums()
    book_num = f"{str(book_nums[book_abbrev]).zfill(2)}"
    html_folder = os.path.join(os.getcwd(), "HTML", f"{book_num}_{book_abbrev}")
    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)

    html_fn = f"{book_abbrev}{chapter.zfill(3)}_word_freq.html"
    with open(os.path.join(html_folder, html_fn), "w", newline="") as write_file:
        write_file.write(filled_in_template)


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
