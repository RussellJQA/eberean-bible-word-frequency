import os

import markdown2  # pip install markdown2

from utils import get_base_template_args, write_html


def write_examples():

    description = "KJV Bible Chapter Word Frequencies: Examples"
    base_template_args = get_base_template_args(
        description,
        ",".join([
            "KJV",
            "Bible",
            "chapter",
            "word frequency",
            "relative frequency",
            "examples",
        ]),
        description,
    )

    with open("examples.md", "r") as read_file:
        examples_source = read_file.read()
    examples_html = markdown2.markdown(examples_source, extras=["tables"])
    examples_html = examples_html.replace('align="right"', 'class="numerical"')
    #   The align attribute which markdown2 puts on th and td elements is
    #   obsolete.
    #   It will fail HTML validation by the W3C's
    #       [Nu Html Checker](https://validator.w3.org/)
    #   Replace it with CSS styling.
    new_template_args = {
        "images_path": "./images",
        "styles_path": "./styles",
        "examples_html": examples_html,
    }

    html_folder = os.path.join(os.getcwd(), "public_html")
    write_html(
        base_template_args,
        new_template_args,
        "templates/examples.mako",
        html_folder,
        "examples.html",
    )


def main():

    write_examples()


if __name__ == "__main__":
    main()
