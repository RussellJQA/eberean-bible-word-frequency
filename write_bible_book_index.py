import os

from get_bible_data import get_bible_books, get_book_nums
from utils import get_base_template_args, write_html

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

    book_nums = get_book_nums()
    book_num = f"{str(book_nums[book_abbrev]).zfill(2)}"
    html_folder = os.path.join(os.getcwd(), "HTML", f"{book_num}_{book_abbrev}")
    write_html(
        base_template_args,
        new_template_args,
        "bible_book_index.mako",
        html_folder,
        f"{book_abbrev}_index.html",
    )


def main():

    write_bible_book_index("Gen")


if __name__ == "__main__":
    main()
