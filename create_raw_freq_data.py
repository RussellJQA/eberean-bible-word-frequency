"""

King James Version + Apocrypha
The King James Version or Authorized Version of the Holy Bible, using the standardized text of 1769, with Apocrypha/Deuterocanon
Public Domain
Language: English
Dialect: archaic British

Letters patent issued by King James with no expiration date means that to print this translation in the United Kingdom or import printed copies into the UK,
you need permission.
Currently, the Cambridge University Press, the Oxford University Press, and Collins have the exclusive right to print this Bible
translation in the UK. This royal decree has no effect outside of the UK, where this work is firmly in the Public Domain.
Please see http://www.cambridge.org/about-us/who-we-are/queens-printers-patent and https://en.wikipedia.org/wiki/King_James_Version#Copyright_status
for more information.
This free text of the King James Version of the Holy Bible is brought to you courtesy of the Crosswire Bible Society and eBible.org.


2018-08-27

"""
# Chapter files extracted from https://ebible.org/Scriptures/eng-kjv_readaloud.zip
# (linked to at https://ebible.org/kjv/)

# Above link and the following copyright information are from:
#   https://ebible.org/find/show.php?id=eng-kjv

import glob
import json
import os.path
import re


def get_full_ref(chapter_file):

    book_number_name_chapter = os.path.basename(chapter_file)[9:-9]
    # basename is, for example, eng-kjv_002_GEN_01_read.txt
    book_abbr = book_number_name_chapter[3:6].title()  # Gen, Exo, ..., Rev
    chapter_number = book_number_name_chapter[7:10].lstrip("0").rstrip("_")
    # Filenames normally contain 2-digit chapter numbers, but have 3 for Psalms
    # Remove leading '0's (as from '01' and '001') and trailing '_'s (as from '01_')

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

    # TODO (possibly): Generate some statistics like mean, median, and mode frequency
    # TODO (possibly): Generate alternative versions with and without italicized words
    frequency_this_passage = {}
    for line in passage:
        line = re.sub(r"[¶’]\S*", "", line).strip()
        # Eliminate paragraph markers, possessives, and leading/trailing blanks
        words = re.sub(r"[^a-z\- ]+", "", line, flags=re.IGNORECASE)
        for word in words.split():
            if word != "LORD":  # Differentiate between "lord"/"Lord" and "LORD"
                # TODO: Possibly do something more generic, like:
                #       if not ((len(word) >= 2) and (word == word.isupper()):
                word = word.casefold()

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

    output_folder = "frequency_jsons"
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    # Write dict of KJV words, each paired (in a list) with its # of occurrences
    # {["a", 8282], ["aaron", 350], ["aaronites", 2], ... ["zuzims", 1]}
    word_frequency_sorted = {}
    for word, count in sorted(word_frequency.items()):
        word_frequency_sorted[word] = count
    with open(os.path.join(output_folder, "word_frequency.json"), "w") as write_file:
        json.dump(word_frequency_sorted, write_file)

    word_frequency_lists = build_frequency_lists(word_frequency)
    with open(os.path.join(output_folder, "word_frequency_lists.json"), "w") as write_file:
        json.dump(word_frequency_lists, write_file, indent=4)

    with open(os.path.join(output_folder, "word_frequency_lists_chapters.json"), "w") as write_file:
        json.dump(frequency_lists_chapters, write_file, indent=4)


def create_raw_freq_data():

    frequency_lists_chapters = {}

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")
    # TODO: Download these files, if needed
    kjv_chapter_files = sorted(glob.glob(os.path.join(source_files, "*.txt")))
    # sorted() because glob() may return the list in an arbitrary order

    for chapter_file in kjv_chapter_files:
        read_file = open(chapter_file, "r", encoding="utf-8")
        lines = read_file.readlines()
        # There's no need to exclude the blank line at the end of chapter files,
        # since readlines() already seems to ignore it.

        full_ref = get_full_ref(chapter_file)

        freq_this_chapter = calc_word_freq(lines[2:])
        frequency_lists_chapters[full_ref] = build_frequency_lists(freq_this_chapter)

    calc_and_write_word_frequency_files(frequency_lists_chapters)

def main():

    create_raw_freq_data()


if __name__ == "__main__":
    main()
