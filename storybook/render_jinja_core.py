import os
import sys
from pathlib import Path

from django.template import engines


def render_macro(template_path, macro_name, content=None, request=None, **context):
    """Render a component through the Jinja engine."""
    template = engines["jinja"].from_string(
        "{% import template_path as component with context %}{{ component[macro_name](**macro_kwargs) }}"
    )
    if content is not None:
        context["content"] = content
    return template.render(
        {"template_path": template_path, "macro_name": macro_name, "macro_kwargs": context},
        request=request,
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('ERROR: Usage: python render_jinja_core.py <template_path> <macro_name> [key="value" ...]')
        sys.exit(1)

    import django

    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))
    sys.path.append(str(root / "ds_judgements_public_ui"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()

    context = {}
    for arg in sys.argv[3:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            stripped_value = value.strip('"').strip("'")
            final_value: bool | int | str
            if stripped_value.lower() == "true":
                final_value = True
            elif stripped_value.lower() == "false":
                final_value = False
            elif stripped_value.isdigit():
                final_value = int(stripped_value)
            else:
                final_value = stripped_value
            context["content" if key == "label" else key] = final_value

    print(render_macro(sys.argv[1], sys.argv[2], **context))
