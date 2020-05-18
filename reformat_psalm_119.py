""" Reformat Psalm 119, by doing the following for each 8-line stanza:
        Enclose it within a pair of opening/closeing paragraph tags (</p> ... <p>)
        Prefix it with the corresponding Hebrew letter (followed by its English name)
"""
import os

HEBREW_LETTER_NAMES = [
    "aleph",
    "beth",
    "gimel",
    "daleth",
    "he",
    "vau",
    "zain",
    "cheth",
    "teth",
    "jod",
    "caph",
    "lamed",
    "mem",
    "nun",
    "samech",
    "ain",
    "pe",
    "tzaddi",
    "koph",
    "resh",
    "schin",
    "tau",
]


def get_hebrew_letter(index):

    alef = "\u05D0"
    return f"{chr(ord(alef) + index)} {HEBREW_LETTER_NAMES[index].upper()}"


def reformat_psalm_119(inp_lines):

    out_lines = []

    for verse, inp_line in enumerate(inp_lines, start=1):

        if (verse % 8) == 1:  # if 1st verse of one of Psalm 119's 22 8-line stanzas
            if verse != 1:
                out_lines.append("\n")
            out_lines.append(
                f"<p>\n                    {get_hebrew_letter(verse // 8)}<br>\n"
            )  # Intentional integer division
        out_lines.append(f"    {verse}: {inp_line.strip()}<br>\n")
        if (verse % 8) == 0:
            out_lines.append("</p>\n")

    return out_lines


def write_reformatted_psalm_119():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_files = os.path.join(script_dir, "downloads", "kjv_chapter_files")

    chapter_file = os.path.join(source_files, "eng-kjv_020_PSA_119_read.txt")
    with open(chapter_file, "r", encoding="utf-8", newline="") as read_file:
        out_lines = reformat_psalm_119(read_file.readlines()[2:])

    reformatted_chapter_file = os.path.join(source_files, "reformatted_psalm119.txt")
    with open(reformatted_chapter_file, "w", encoding="utf-8") as write_file:
        write_file.writelines(out_lines)


def main():

    write_reformatted_psalm_119()


if __name__ == "__main__":
    main()
