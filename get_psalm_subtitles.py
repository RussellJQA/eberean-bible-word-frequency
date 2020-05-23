import os.path
import re


def get_psalm_subtitles():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    psalms_with_subtitles = os.path.join(script_dir, "downloads", "Psalms.txt")

    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    with open(psalms_with_subtitles, "r", encoding="utf-8") as read_file:
        lines = read_file.readlines()

    subtitles = os.path.join(data_dir, "subtitles.txt")
    with open(subtitles, "w", encoding="utf-8") as write_file:
        previous_psalm_title_loc = None
        for line_count, line in enumerate(lines, start=1):
            psalm_title_pattern = r"(^Psalm \d{1,3}$)"
            match = re.search(psalm_title_pattern, line)
            if match:
                psalm_title = line.strip()
                previous_psalm_title_loc = line_count
            elif (
                previous_psalm_title_loc and line_count == previous_psalm_title_loc + 2
            ):
                if line[0] != "{":
                    subtitle = line.strip()
                    # print(f"{psalm_title}\t{subtitle}")
                    write_file.write(f"{psalm_title}\t{subtitle}\n")


def main():

    get_psalm_subtitles()


if __name__ == "__main__":
    main()
