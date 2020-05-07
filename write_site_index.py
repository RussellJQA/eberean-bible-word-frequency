import markdown2  # pip install markdown2
import os

from get_bible_data import get_bible_books, get_book_nums
from utils import get_base_template_args, write_html


def write_site_index():

    description = "KJV Bible Chapter Word Frequencies"
    base_template_args = get_base_template_args(
        description,
        ",".join(["KJV", "Bible", "chapter", "word frequency"]),
        "Home: " + description,
    )

    with open("readme.md", "r") as read_file:
        readme_source = read_file.read()
    readme_html = markdown2.markdown(readme_source)
    readme_html = readme_html.replace("examples.md", "examples.html")
    #   GitHub repos's README.md file points to GitHub repos's examples.md file
    #   Update to point to corresponding examples.html file
    bible_books = get_bible_books()
    book_nums = get_book_nums()
    new_template_args = {
        "resources_path": ".",
        "readme_html": readme_html,
        "bible_books": bible_books,
        "book_nums": book_nums,
    }

    html_folder = os.path.join(os.getcwd(), "HTML")
    write_html(
        base_template_args,
        new_template_args,
        "site_index.mako",
        html_folder,
        "index.html",
    )


def main():

    write_site_index()


if __name__ == "__main__":
    main()
