import json
import os

import requests  # pip install requests


def get_binary_file_via_from_web(
    web_folder, binary_file, download_folder, re_download=False
):

    download_file = os.path.join(download_folder, binary_file)
    if re_download or not os.path.exists(download_file):
        binary_url = web_folder + binary_file
        resp = requests.get(binary_url)
        if resp.status_code == 200:
            with open(download_file, "wb") as write_file:
                write_file.write(resp.content)
        else:
            print(f"Download failed with status code: {resp.status_code}")


def get_web_json_data(web_folder, json_fn, download_folder):

    """ Gets JSON data from the Web.
    """

    if not os.path.isdir(download_folder):
        os.mkdir(download_folder)

    json_path = os.path.join(download_folder, json_fn)
    if not os.path.exists(json_path):
        get_binary_file_via_from_web(web_folder, json_fn, download_folder)

    with open(json_path, "r") as read_file:
        json_data = json.load(read_file)
        return json_data


def get_bible_books():

    web_folder = (
        r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "bible_books.json", "downloads")


def get_book_nums():

    web_folder = (
        r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "book_numbers.json", "downloads")


def get_verse_counts():

    web_folder = (
        r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    )
    return get_web_json_data(web_folder, "verse_counts_by_chapter.json", "downloads")


def main():

    bible_books = get_bible_books()
    if len(bible_books) != 66:
        print(
            f"The Bible has 66 books, but 'bible_books' has {len(bible_books)} books."
        )

    book_nums = get_book_nums()
    if len(book_nums) != 66:
        print(f"The Bible has 66 books, but 'book_nums' has {len(book_nums)} books.")

    verse_counts_by_chapter = get_verse_counts()
    if len(verse_counts_by_chapter) != 1189:
        print(
            f"The Bible has 1,189 chapters, but 'verse_counts_by_chapter' has {len(verse_counts_by_chapter)} chapters."
        )


if __name__ == "__main__":
    main()
