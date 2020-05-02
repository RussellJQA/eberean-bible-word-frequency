"""
Calculates the relative frequencies of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os

from get_files_and_data import get_book_nums, get_bible_books
from create_raw_freq_data import create_raw_freq_data, get_word_frequency
from write_bible_book_index import write_bible_book_index
from write_bible_chapter import write_bible_chapter

bible_books = get_bible_books()
book_lengths = {
    bible_books[bible_book][0]: bible_books[bible_book][1] for bible_book in bible_books
}


def round_4_to_6_sigfigs(num):
    """ If there are more than 4 significant figures to the left of the decimal point:
            Round to the number of sigfits to the left of the decimal point
        Else:
            Round to 4 sigfigs
        Rounding based on:
            https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python/3411731
    NOTE: For words_in_bible = 790663,
          we only need to allow for up to 6 sigfigs to the left of the decimal point
    """
    if num >= (10 ** 5):
        return int("%.6g" % num)
    if num >= (10 ** 4):
        return int("%.5g" % num)
    if num >= (10 ** 3):
        return int("%.4g" % num)
    return float("%.4g" % num)


def sort_desc_by_simple_desc_by_weighted_asc_by_word(element):

    sort_key = (-1 * element[1][2], -1 * element[1][3], element[0])
    # -1 * simple_relative_frequency, -1 * weighted_relative_frequency, word

    return sort_key


def handle_book_folder(html_folder, book_folder, previous_book_abbrev, book_abbrev):

    if previous_book_abbrev != book_abbrev:
        book_nums = get_book_nums()
        book_num_name = f"{str(book_nums[book_abbrev]).zfill(2)}_{book_abbrev}"
        book_folder = os.path.join(html_folder, book_num_name)
        if not os.path.isdir(book_folder):
            os.mkdir(book_folder)

    return book_folder


def get_chapter_word_freqs(
    words_in_bible, words_in_chapter, word_frequencies, word_frequency
):

    chapter_word_freqs = {}
    for (chapter_frequency, words) in word_frequencies.items():
        if words != ["TOTAL WORDS"]:
            times_in_chapter = int(chapter_frequency)
            for word in words:
                times_in_bible = word_frequency[word]

                simple_relative_frequency = (
                    words_in_bible * times_in_chapter
                ) / times_in_bible
                # Equivalently: words_in_bible * (times_in_chapter / times_in_bible)

                values = [
                    times_in_chapter,
                    times_in_bible,
                    round_4_to_6_sigfigs(simple_relative_frequency),
                    # Below is weighted_relative_frequency (rounded)
                    round_4_to_6_sigfigs(
                        (simple_relative_frequency / words_in_chapter)
                        + (times_in_chapter - 1)
                    ),
                ]

                # weighted_relative_frequency was chosen so that (for example) for Exodus 5's:
                #    8 out of 16 occurrences of straw
                #    1 out of 2 occurrences of dealest
                # weighted_relative_frequency for "straw" would be greater than for "dealest"

                # The print() statements below were used (1 at a time) to help me
                # to determine what to use for weighted_relative_frequency.

                # if times_in_chapter == times_in_bible:
                #     print(f"\tAll {times_in_chapter} occurrences of {word}")

                # if 2 * times_in_chapter == times_in_bible:
                #     print(
                #         f"\t{times_in_chapter} out of {times_in_bible} occurrences of {word}"
                #     )

                chapter_word_freqs[word] = values

    return chapter_word_freqs


def get_relative_word_frequency(
    words_in_bible, words_in_chapter, word_frequencies, word_frequency
):

    relative_word_frequency = {}
    relative_word_frequency["TOTAL WORDS"] = [words_in_chapter]
    chapter_word_freqs = get_chapter_word_freqs(
        words_in_bible, words_in_chapter, word_frequencies, word_frequency
    )
    for chapter_word_freq, values in sorted(
        chapter_word_freqs.items(), key=sort_desc_by_simple_desc_by_weighted_asc_by_word
    ):
        relative_word_frequency[chapter_word_freq] = values

    return relative_word_frequency


def write_csv_file(words_in_bible, key, csv_fn, relative_word_frequency):

    with open(csv_fn, mode="w", newline="") as csv_file:
        # newline="" prevents blank lines from being added between rows
        writer = csv.writer(csv_file, delimiter=",", quotechar='"')
        writer.writerow(
            ["word", "numInChap", "numInKjv", "simpleRelFreq", "weightedRelFreq",]
        )
        #   Column header row

        for count, chapter_word_freq in enumerate(relative_word_frequency):
            values = relative_word_frequency[chapter_word_freq]
            if count:  # Data row
                writer.writerow(
                    [chapter_word_freq, values[0], values[1], values[2], values[3],]
                )
            else:  # Totals row
                writer.writerow(
                    [
                        f"TOTAL ({key})",
                        relative_word_frequency[chapter_word_freq][0],
                        words_in_bible,
                    ]
                )


def write_html_file(book_abbrev, chapter, words_in_chapter, relative_word_frequency):

    # TODO: Can a dictionary comprehension be used here?
    #   (May have to first remove the "TOTAL WORDS" entry.)

    rows = []
    for item in relative_word_frequency.items():
        if item[0] != "TOTAL WORDS":
            num_in_kjv = "{:,}".format(
                item[1][1]
            )  # Add thousands separator (e.g., 1234 -> "1,234")
            simple_relative_frequency = "{:,}".format(item[1][2])
            row = [
                item[0],
                item[1][0],
                num_in_kjv,
                simple_relative_frequency,
                item[1][3],
            ]
            #  .csv column headings: word, numInChap, numInKjv, simpleRelFreq, weightedRelFreq
            rows.append(row)
    write_bible_chapter(book_abbrev, chapter, words_in_chapter, rows)


def write_csv_and_html(
    words_in_bible, key, book_abbrev, book_folder, relative_word_frequency
):

    book_abbrev = key[0:3]
    chapter = key[4:]

    csv_fn = os.path.join(book_folder, f"{book_abbrev}{chapter.zfill(3)}_word_freq.csv")
    write_csv_file(words_in_bible, key, csv_fn, relative_word_frequency)

    # In addition to the above .csv file, generate an .html file with sortable tables
    # Currently, that's done with method #1 below, but we may want to look at some of
    # other alternatives:
    #  *1. https://www.kryogenix.org/code/browser/sorttable/sorttable.js
    #   2. https://www.w3schools.com/howto/howto_js_sort_table.asp
    # **3. https://brython.info/gallery/sort_table.html
    # ***4. https://brython.info/gallery/sort_table_template.html
    #   5. https://stefanhoelzl.github.io/vue.py/examples/grid_component/
    #       source at
    #       https://github.com/stefanhoelzl/vue.py/blob/master/examples/grid_component/app.py
    #   6. https://anvil.works/docs/data-tables/data-tables-in-code#searching-querying-a-table

    words_in_chapter = "{:,}".format(relative_word_frequency["TOTAL WORDS"][0])
    write_html_file(book_abbrev, chapter, words_in_chapter, relative_word_frequency)


def generate_word_freq_files():

    # TODO:
    # Refactor using a function which instead of calculating word frequencies in a chapter
    # relative to word frequencies in the Bible,
    # calculates word frequencies in a subunit, relative to word frequencies in a unit.
    # Such a function might be used for calculating (relative) word frequencies for the OT, NT,
    # individual book, daily readings, etc.

    words_in_bible = 790663
    word_frequency = get_word_frequency()
    chapters_relative_word_frequency = {}

    frequency_jsons = os.path.join(os.getcwd(), "frequency_jsons")
    if not os.path.isdir(frequency_jsons):
        os.mkdir(frequency_jsons)

    previous_book_abbrev = ""
    book_folder = ""

    read_fn = os.path.join(frequency_jsons, "word_frequency_lists_chapters.json")
    if not os.path.exists(read_fn):
        create_raw_freq_data()

    with open(read_fn, "r") as read_file:

        html_folder = os.path.join(os.getcwd(), "HTML")
        if not os.path.isdir(html_folder):
            os.mkdir(html_folder)

        word_frequency_lists_chapters = json.load(read_file)
        for (key, word_frequencies) in word_frequency_lists_chapters.items():

            # print(key)

            words_in_chapter = int(next(iter(word_frequencies)))
            relative_word_frequency = get_relative_word_frequency(
                words_in_bible, words_in_chapter, word_frequencies, word_frequency
            )
            chapters_relative_word_frequency[key] = relative_word_frequency

            book_abbrev = key[0:3]
            book_folder = handle_book_folder(
                html_folder, book_folder, previous_book_abbrev, book_abbrev
            )
            if book_abbrev != previous_book_abbrev:
                write_bible_book_index(book_abbrev)
            write_csv_and_html(
                words_in_bible, key, book_abbrev, book_folder, relative_word_frequency
            )

            previous_book_abbrev = book_abbrev

    # TODO: Write master index file

    write_fn = os.path.join(frequency_jsons, r"chapters_relative_word_frequency.json")
    with open(write_fn, "w") as write_file:
        json.dump(chapters_relative_word_frequency, write_file, indent=4)


def main():
    generate_word_freq_files()


if __name__ == "__main__":
    main()
