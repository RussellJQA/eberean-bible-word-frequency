import os

from get_bible_data import get_bible_books, get_book_nums
from utils import get_base_template_args, write_html


def write_bible_book_index(book_abbrev):

    bible_books = get_bible_books()
    bible_book_names = {
        bible_books[bible_book][0]: bible_book for bible_book in bible_books
    }
    bible_book_name = bible_book_names[book_abbrev]
    book_length = bible_books[bible_book_name][1]

    description = f"KJV Bible Chapter Word Frequencies: {bible_book_name}"
    base_template_args = get_base_template_args(
        description,
        ",".join(["KJV", "Bible", bible_book_name, "chapter", "word frequency"]),
        description,
    )

    new_template_args = {
        "images_path": "../images",
        "styles_path": "../styles",
        "bible_book_name": bible_book_name,
        "book_abbrev": book_abbrev,
        "chapters_in_book": book_length,
    }

    book_num = f"{str(get_book_nums()[book_abbrev]).zfill(2)}"
    html_folder = os.path.join(os.getcwd(), "public_html")
    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)
    chapter_folder = os.path.join(html_folder, f"{book_num}-{book_abbrev.lower()}")
    if not os.path.isdir(chapter_folder):
        os.mkdir(chapter_folder)
    write_html(
        base_template_args,
        new_template_args,
        "templates/bible_book_index.mako",
        chapter_folder,
        f"{book_abbrev.lower()}-index.html",
    )


def main():

    write_bible_book_index("Gen")


if __name__ == "__main__":
    main()
