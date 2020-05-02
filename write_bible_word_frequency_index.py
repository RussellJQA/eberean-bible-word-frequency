import os

from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako

from get_bible_data import get_bible_books
from utils import get_base_template_args

template_lookup = TemplateLookup([""])
raw_template = Template(
    filename="bible_word_frequency_index_template.mako", lookup=template_lookup
)

bible_books = get_bible_books()
book_lengths = {
    bible_books[bible_book][0]: bible_books[bible_book][1] for bible_book in bible_books
}


def write_bible_word_frequency_index():
    base_template_args = get_base_template_args("Bible (KJV) Chapter Word Frequencies")

    new_template_args = {}

    # Merge dictionaries
    filled_in_template_args = {**base_template_args, **new_template_args}
    # In Python 3.9, PEP 584 will let you merge  2 dicts using | or |=
    filled_in_template = raw_template.render(**filled_in_template_args)

    html_folder = os.path.join(os.getcwd(), "HTML")
    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)

    html_fn = "bible_word_frequency_index.html"
    with open(os.path.join(html_folder, html_fn), "w", newline="") as write_file:
        write_file.write(filled_in_template)


def main():

    write_bible_word_frequency_index()


if __name__ == "__main__":
    main()
