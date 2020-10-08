import collections
import glob
import os
import re

# TODOs:
# function to sum word frequencies?
#     chapters -> books
#         books -> testaments
#             testaments -> Bible
#
# iteration functions
#     on subsection change
#         set section frequency
#     on done
#         final settings of section frequency
#
# AND/OR, perhaps a function like get_counter() below.


def get_counter(lines):

    word_counter = collections.Counter()

    # TODO: See if there's a place for using Counter's methods
    # [elements(), most_common(), subtract(), and/or update()]
    # or Counter's arithmetic operators (+, -, &, and/or |).
    # See pymotw.com/2/collections/counter.html and
    # guru99.com/python-counter-collections-example.html

    # TODO: See if there's a place to use collections.defaultdict

    for line in lines:  # Split multi-line string into list of lines

        # Eliminate paragraph markers, possessives, and
        # leading/trailing whitespace
        line = re.sub(r"[¶’]\S*", "", line).strip()
        words = re.sub(r"[^a-zæ\- ]+", "", line, flags=re.IGNORECASE)

        words2 = [
            (word if (word == "LORD") else word.casefold())
            #   Differentiate between "lord"/"Lord" and "LORD"
            #   casefold() is a more aggressive lower() alternative
            for word in words.split()
        ]

        word_counter.update(words2)

    return word_counter


def test_counters():

    source_files = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "downloads", "kjv_chapter_files")

    book_counter = collections.Counter()
    for chapter_file in [
            "eng-kjv_002_GEN_01_read.txt", "eng-kjv_002_GEN_02_read.txt"
    ]:

        chapter_path = os.path.join(source_files, chapter_file)

        with open(chapter_path, "r", encoding="utf-8") as read_file:

            lines = read_file.readlines()

            chapter_counter = get_counter(lines)
            print(f"\n{chapter_file}")
            print(chapter_counter)

            book_counter.update(chapter_counter)

    print(f"\nGenesis:\n{book_counter}")


def test_match_counts_in_csvs():

    subfolders = os.scandir(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     "public_html"))

    for subfolder in subfolders:
        match_counts = []
        if subfolder.is_dir():
            csv_files = sorted(glob.glob(os.path.join(subfolder, "*.csv")))
            if csv_files:
                print(subfolder.name)
                for csv_file in csv_files:
                    with open(csv_file, "r", encoding="utf-8") as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if line[0:4] == "the,":
                                second_comma_loc = line.find(",", 4)
                                match_counts.append(line[4:second_comma_loc])

                total_match_counts = 0
                for match_count in match_counts:
                    total_match_counts += int(match_count)
                print(total_match_counts)


def print_match_info(weighted_pattern_match, total_line):

    rounded_weighted_freq = float(weighted_pattern_match.group(7))
    total_pattern = (
        r"TOTAL \(([0-9A-ZÆa-zæ]{3}) ([0-9]{1,3})\),([0-9]{1,4}),([0-9]{6})")

    if 0.9999 <= rounded_weighted_freq <= 1.0001:
        match = re.search(total_pattern, total_line)
        if match:
            word = weighted_pattern_match.group(1)
            num_in_chapter = int(weighted_pattern_match.group(3))
            num_in_kjv = int(weighted_pattern_match.group(5))
            weighted_freq1 = "{:.4f}".format(rounded_weighted_freq)

            book = match.group(1)
            chapter = match.group(2)
            words_in_chapter = int(match.group(3))
            words_in_kjv = int(match.group(4))

            simple_freq = words_in_kjv * num_in_chapter / num_in_kjv
            weighted_freq2 = "{:.16f}".format((simple_freq /
                                               words_in_chapter) +
                                              (num_in_chapter - 1))

            print(
                f"{weighted_freq2} {weighted_freq1} {book} {chapter}: {word}")
        else:
            print("No match")


def find_weighted_near_one():

    weighted_pattern = \
        "([A-ZÆa-zæ]*)(,)([0-9.]*)(,)([0-9.]*)(,[0-9.]*,)([0-9.]*$)"
    subfolders = os.scandir(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     "public_html"))

    for subfolder in subfolders:
        if subfolder.is_dir():
            csv_files = sorted(glob.glob(os.path.join(subfolder, "*.csv")))
            if csv_files:
                for csv_file in csv_files:
                    with open(csv_file, "r", encoding="utf-8") as read_file:
                        lines = read_file.readlines()
                        for line in lines[2:]:
                            # Exclude 1st 2 lines,
                            # since they're header info like:
                            #   word,numInChap,numInKjv,simpleRelFreq,
                            #       weightedRelFreq
                            #   TOTAL (Gen 1),797,790663

                            weighted_pattern_match = re.search(
                                weighted_pattern, line)
                            if weighted_pattern_match:
                                print_match_info(
                                    weighted_pattern_match,
                                    total_line=lines[1],
                                )
    # The output, sorted is:
    # 1.0001960764470443 1.0000 1Sa 10: away
    # 0.9998925068416233 0.9999 2Sa 4: children
    # 0.9998773331984420 0.9999 2Ch 1: go
    # 1.0004947663589245 1.0000 Neh 7: again
    # 1.0003049004202818 1.0000 Psa 2: will
    # 1.0001960764470443 1.0000 Isa 5: among
    # 1.0001189017024448 1.0000 Isa 37: word
    # 1.0004188113349834 1.0000 Isa 39: are
    # 1.0000366794243607 1.0000 Jer 31: egypt  {Best "match" [closest to 1.0]}
    # 1.0000366794243607 1.0000 Jer 31: holy
    # 0.9998988293288718 0.9999 Mic 5: also
    # 0.9998925068416233 0.9999 Luk 18: put
    # 0.9998571023905631 0.9999 Act 9: nor
    # 0.9998621600157821 0.9999 2Co  come
    # 1.0004947663589245 1.0000 Heb 10: over
    # 1.0003352741277181 1.0000 Rev 16: even

    # EXAMPLE for understanding weighted relative frequency:

    # word,numInChap,numInKjv,simpleRelFreq,weightedRelFreq
    # TOTAL (Jer 31),1294,790663
    # ...
    # egypt,1,611,1294,1.0

    # There is 1 occurrence of "egypt" in this 1294-word chapter

    # That's what you'd expect, given that:
    #   There are 611 occurrences in the 790663-word Bible.
    # You'd expect 1294 * 611/790663 occurrences in a 1294-word chapter =
    #     (1294 * 611) / 790663 = 790634 / 790663 = 0.99996332192097012254
    # which rounded to the nearest integer is certainly 1.


def main():

    # test_counters()
    # test_match_counts_in_csvs()
    find_weighted_near_one()


if __name__ == "__main__":
    main()
