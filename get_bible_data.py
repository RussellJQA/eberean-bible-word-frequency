import json
import os

from utils import get_binary_file_via_from_web


def get_web_json_data(web_folder, json_fn, download_folder):

    """ Gets JSON data from the Web.
    """

    os.makedirs(download_folder, exist_ok=True)
    json_path = os.path.join(download_folder, json_fn)
    if not os.path.exists(json_path):
        get_binary_file_via_from_web(web_folder, json_fn, download_folder)

    with open(json_path, "r") as read_file:
        json_data = json.load(read_file)
        return json_data


def get_bible_books():

    web_folder = (
        "https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "bible_books.json", "downloads")


def get_book_nums():

    web_folder = (
        "https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "book_numbers.json", "downloads")


def get_verse_counts():

    web_folder = (
        "https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "verse_counts_by_chapter.json", "downloads")


def main():

    bible_books = get_bible_books()
    if (books := len(bible_books)) != 66:
        print(f"The Bible has 66 books, but 'bible_books' has {books} books.")

    book_nums = get_book_nums()
    if (books := len(book_nums)) != 66:
        print(f"The Bible has 66 books, but 'book_nums' has {books} books.")

    verse_counts_by_chapter = get_verse_counts()
    if (chapters := len(verse_counts_by_chapter)) != 1189:
        print(
            f"The Bible has 1,189 chapters, but 'verse_counts_by_chapter' has {chapters} chapters."
        )


if __name__ == "__main__":
    main()
