import json
import os
import re

# TODO: Add these subtitles to (copies of) the KJV Psalm chapter files


def get_subtitles():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    psalms_with_subtitles = os.path.join(script_dir, "downloads", "Psalms.txt")

    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    with open(psalms_with_subtitles, "r", encoding="utf-8") as read_file:
        lines = read_file.readlines()

    subtitles = {}
    previous_psalm_title_loc = None
    for line_count, line in enumerate(lines, start=1):
        psalm_title_pattern = r"^Psalm (\d{1,3})$"
        match = re.search(psalm_title_pattern, line)
        if match:
            psalm_title = match.group(1)
            previous_psalm_title_loc = line_count
        elif previous_psalm_title_loc and line_count == previous_psalm_title_loc + 2:
            if line[0] != "{":
                subtitle = line.strip()
                subtitles[psalm_title] = subtitle

    return subtitles


def write_subtitles():

    subtitles = get_subtitles()
    output_folder = "data"
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "subtitles.json"), "w") as write_file:
        json.dump(subtitles, write_file, indent=4)


def main():

    write_subtitles()


if __name__ == "__main__":
    main()
