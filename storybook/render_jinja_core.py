import os
import sys

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    PrefixLoader,
)

# -----------------------------
# Jinja template root (project)
# -----------------------------
JINJA_TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), "..", "ds_judgements_public_ui", "templates")


# -----------------------------
# Fake url function for Storybook
# -----------------------------
def fake_url(name):
    """Simulate Django's url() for Jinja templates in Storybook."""
    return f"/{name}/"


# -----------------------------
# Fake static() function
# -----------------------------
def fake_static(path):
    """Simulate Django's static() for Storybook."""
    return f"http://localhost:3000/static/{path}"


# -----------------------------
# Jinja loaders
# -----------------------------
project_loader = FileSystemLoader(JINJA_TEMPLATE_ROOT)

govuk_loader = PrefixLoader(
    {
        "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
    }
)

# -----------------------------
# Jinja Environment
# -----------------------------
env = Environment(
    loader=ChoiceLoader([project_loader, govuk_loader]),
    autoescape=True,
)

env.globals["url"] = fake_url
env.globals["static"] = fake_static


# -----------------------------
# Fake hyphenate filter
# -----------------------------
def hyphenate(value):
    """Simulate Django/GOV.UK hyphenate filter for Storybook."""
    if value is None:
        return ""
    return str(value).replace(" ", "-")


env.filters["hyphenate"] = hyphenate


# -----------------------------
# Render a macro with optional caller() content
# -----------------------------
def render_macro(template_path, macro_name, content=None, **context):
    try:
        template = env.get_template(template_path)
        macro = getattr(template.module, macro_name)

        if content is not None:
            return macro.__call__(content, **context)
        else:
            return macro(**context)

    except Exception as e:
        return f"Error rendering macro: {e}"


# -----------------------------
# Command-line execution
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('ERROR: Usage: python render_jinja_core.py <template_path> <macro_name> [key="value" ...]')
        sys.exit(1)

    template_path = sys.argv[1]
    macro_name = sys.argv[2]

    context = {}
    macro_content = None

    for arg in sys.argv[3:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            stripped_value = value.strip('"').strip("'")

            if stripped_value.lower() == "true":
                final_value = True
            elif stripped_value.lower() == "false":
                final_value = False
            elif stripped_value.isdigit():
                final_value = int(stripped_value)
            else:
                final_value = stripped_value

            if key == "label":
                macro_content = final_value
            else:
                context[key] = final_value

    html = render_macro(template_path, macro_name, content=macro_content, **context)
    print(html)
