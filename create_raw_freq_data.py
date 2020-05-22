import glob
import json
import os.path
import re

from utils import mkdir_if_not_isdir
from get_downloads import get_downloads


def get_full_ref(chapter_file):

    book_number_name_chapter = os.path.basename(chapter_file)[9:-9]
    # basename is, for example, eng-kjv_002_GEN_01_read.txt
    book_abbr = book_number_name_chapter[3:6].title()  # Gen, Exo, ..., Rev
    chapter_number = book_number_name_chapter[7:10].lstrip("0").rstrip("_")
    # Filenames normally contain 2-digit chapter numbers, but have 3 for Psalms
    # Remove leading 0s (as from "01" and "001") and trailing "_"s (as from "01_")

    # Calculate verse counts
    full_ref = book_abbr + " " + chapter_number
    return full_ref


def desc_value_asc_key(element):

    sort_key = (-1 * element[1], element[0])
    return sort_key


def build_frequency_lists(frequency):

    total_words = 0  # The final value of total_words is 790,663
    words_with_this_frequency = []
    frequency_lists = {}
    prev_occurrences = 0
    occurrences = 0
    for element in sorted(frequency.items(), key=desc_value_asc_key):
        # Split into lists of words for each frequency:
        word = element[0]
        occurrences = element[1]  # For "the", occurrences is 64016
        total_words += occurrences
        if prev_occurrences and occurrences != prev_occurrences:
            frequency_lists[prev_occurrences] = words_with_this_frequency[:]
            words_with_this_frequency.clear()
        words_with_this_frequency.append(word)
        prev_occurrences = occurrences
    frequency_lists[occurrences] = words_with_this_frequency[:]
    frequency_lists = {total_words: ["TOTAL WORDS"], **frequency_lists}

    total_words2 = 0  # Essentially, recalc total_words a 2nd way, for comparison.
    for key, value in sorted(frequency_lists.items(), reverse=True):
        if value != ["TOTAL WORDS"]:
            total_words2 += int(key) * len(value)
            # Increment by number of occurrences * number of words with that number
    if total_words != total_words2:
        print(f"total_words ({total_words}) != to total_words2 ({total_words2})")

    return frequency_lists


def calc_word_freq(passage):

    # TODO (possibly): Generate alternative versions with and without italicized words

    frequency_this_passage = {}
    for line in passage:

        line = re.sub(r"[¶’]\S*", "", line).strip()
        # Eliminate paragraph markers, possessives, and leading/trailing whitespace

        words = re.sub(r"[^a-z\- ]+", "", line, flags=re.IGNORECASE)

        for word in words.split():

            if word != "LORD":  # Differentiate between "lord"/"Lord" and "LORD"
                # TODO: Possibly do something more generic, like:
                #       if not ((len(word) >= 2) and (word == word.isupper()):
                word = word.casefold()
                # NOTE: casefold() is an alternative to lower() that [unlike lower()]
                # also lowercases non-ASCII characters

            if word in frequency_this_passage:
                frequency_this_passage[word] += 1
            else:
                frequency_this_passage[word] = 1

    return frequency_this_passage


def calc_and_write_word_frequency_files(frequency_lists_chapters):

    word_frequency = {}
    for (_, frequency_list) in frequency_lists_chapters.items():
        for count, words in frequency_list.items():
            if words != ["TOTAL WORDS"]:
                for word in words:
                    if word in word_frequency:
                        word_frequency[word] += count
                    else:
                        word_frequency[word] = count

    output_folder = "data"
    mkdir_if_not_isdir(output_folder)

    # Write dict of KJV words, each paired (in a list) with its # of occurrences
    # {["a", 8282], ["aaron", 350], ["aaronites", 2], ... ["zuzims", 1]}
    word_frequency_sorted = {}
    for word, count in sorted(word_frequency.items()):
        word_frequency_sorted[word] = count
    with open(os.path.join(output_folder, "word_frequency.json"), "w") as write_file:
        json.dump(word_frequency_sorted, write_file)

    word_frequency_lists = build_frequency_lists(word_frequency)
    with open(
        os.path.join(output_folder, "word_frequency_lists.json"), "w"
    ) as write_file:
        json.dump(word_frequency_lists, write_file, indent=4)

    with open(
        os.path.join(output_folder, "word_frequency_lists_chapters.json"), "w"
    ) as write_file:
        json.dump(frequency_lists_chapters, write_file, indent=4)


def create_raw_freq_data():

    frequency_lists_chapters = {}

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")

    get_downloads()  # Download KJV chapter files, if needed
    kjv_chapter_files = sorted(glob.glob(os.path.join(source_files, "*.txt")))
    # sorted() because glob() may return the list in an arbitrary order

    for chapter_file in kjv_chapter_files:

        if not chapter_file.endswith("eng-kjv_000_000_000_read.txt"):
            #   Ignore what's essentially a README.txt file

            with open(chapter_file, "r", encoding="utf-8") as read_file:

                lines = read_file.readlines()
                # There's no need to exclude the blank line at the end of chapter files,
                # since readlines() already seems to ignore it.

                full_ref = get_full_ref(chapter_file)

                freq_this_chapter = calc_word_freq(lines[2:])
                frequency_lists_chapters[full_ref] = build_frequency_lists(
                    freq_this_chapter
                )

    calc_and_write_word_frequency_files(frequency_lists_chapters)


def get_word_frequency():

    json_path = os.path.join("data", "word_frequency.json")
    if not os.path.exists(json_path):
        create_raw_freq_data()

    with open(json_path, "r") as read_file:
        json_data = json.load(read_file)
        return json_data


def main():

    word_frequency = get_word_frequency()
    expected_num_words = 12553
    if (num_words := len(word_frequency)) != expected_num_words:
        print(
            f"\nThe number of unique words was {num_words}, rather than the expected {expected_num_words}.\n"
        )


if __name__ == "__main__":
    main()
