import os

from mako.template import Template  # pip install Mako
from mako.lookup import TemplateLookup  # pip install Mako
import markdown2  # pip install markdown2

from utils import get_base_template_args

template_lookup = TemplateLookup([""])
raw_template = Template(filename="examples.mako", lookup=template_lookup)


def write_examples():

    html_folder = os.path.join(os.getcwd(), "HTML")
    if not os.path.isdir(html_folder):
        os.mkdir(html_folder)

    description = "Examples"
    base_template_args = get_base_template_args(
        description,
        ",".join(
            [
                "KJV",
                "Bible",
                "chapter",
                "word frequency",
                "relative frequency",
                "examples",
            ]
        ),
        description,
    )

    with open("examples.md", "r") as read_file:
        examples_source = read_file.read()

    examples_html = markdown2.markdown(examples_source, extras=["tables"])
    examples_html = examples_html.replace('align="right"', 'class="numerical"')

    new_template_args = {
        "style_sheet_path": r"./style.css",
        "examples_html": examples_html,
    }

    # Merge dictionaries
    filled_in_template_args = {**base_template_args, **new_template_args}
    # In Python 3.9, PEP 584 will let you merge  2 dicts using | or |=
    filled_in_template = raw_template.render(**filled_in_template_args)

    with open(
        os.path.join(html_folder, "examples.html"), "w", newline=""
    ) as write_file:
        write_file.write(filled_in_template)


def main():

    write_examples()


if __name__ == "__main__":
    main()
