import json
import os
import requests


def get_binary_file_via_requests(web_folder, binary_file, download_folder, re_download=False):

    download_file = os.path.join(download_folder, binary_file)
    if re_download or not os.path.exists(download_file):  
        binary_url = web_folder + binary_file
        resp = requests.get(binary_url)
        if resp.status_code == 200:
            with open(download_file, "wb") as write_file:
                write_file.write(resp.content)
        else:
            print(f"Download failed with status code: {resp.status_code}")


def get_json_data(web_folder, json_fn, download_folder):

    if not os.path.isdir(download_folder):
        os.mkdir(download_folder)

    json_path = os.path.join(download_folder, json_fn)
    if not os.path.exists(json_path):
        get_binary_file_via_requests(web_folder, json_fn, download_folder)

    with open(json_path, "r") as read_file:
        json_data = json.load(read_file)
        return json_data


def get_bible_books():

    web_folder = r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    return get_json_data(web_folder, "bible_books.json", "downloads")


def get_word_frequency():

    web_folder = r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    return get_json_data(web_folder, "word_frequency.json", "downloads")


def get_book_nums():

    web_folder = r"https://raw.githubusercontent.com/RussellJQA/eBEREAN/master/BibleMetaData/"
    return get_json_data(web_folder, "book_numbers.json", "downloads")


def main():

    # TODO: Suppress pylint errors properly

    bible_books = get_bible_books()
    print(type(bible_books))  # Use bible_books to avoid pylint error

    word_frequency = get_word_frequency()
    print(type(word_frequency))  # Use word_frequency to avoid pylint error

    book_nums = get_book_nums()
    print(type(book_nums))  # Use book_nums to avoid pylint error


if __name__ == "__main__":
    main()
