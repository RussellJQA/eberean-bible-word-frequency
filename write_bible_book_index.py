import os

from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako

from get_bible_data import get_bible_books, get_book_nums
from utils import get_base_template_args

template_lookup = TemplateLookup([""])
raw_template = Template(filename="bible_book_index.mako", lookup=template_lookup)

bible_books = get_bible_books()
book_lengths = {
    bible_books[bible_book][0]: bible_books[bible_book][1] for bible_book in bible_books
}
bible_book_names = {
    bible_books[bible_book][0]: bible_book for bible_book in bible_books
}


def write_bible_book_index(book_abbrev):

    description = f"KJV Bible Chapter Word Frequencies: {bible_book_names[book_abbrev]}"

    base_template_args = get_base_template_args(
        description,
        ",".join(
            ["KJV", "Bible", bible_book_names[book_abbrev], "chapter", "word frequency"]
        ),
        description,
    )

    new_template_args = {
        "style_sheet_path": r"../style.css",
        "bible_book_name": bible_book_names[book_abbrev],
        "book_abbrev": book_abbrev,
        "chapters_in_book": book_lengths[book_abbrev],
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

    html_fn = f"{book_abbrev}_index.html"
    with open(os.path.join(html_folder, html_fn), "w", newline="") as write_file:
        write_file.write(filled_in_template)


def main():

    write_bible_book_index("Gen")


if __name__ == "__main__":
    main()
