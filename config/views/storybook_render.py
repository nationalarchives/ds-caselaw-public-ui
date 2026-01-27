import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .render_jinja_core import render_macro


@csrf_exempt
def storybook_render_view(request):
    if request.method != "POST":
        return HttpResponse("POST required", status=400)

    try:
        data = json.loads(request.body)
        template_path = data.get("template")  # e.g., "components/button_examples.jinja"
        macro_name = data.get("macro")  # e.g., "default" or "button"
        args = data.get("args", {})  # Storybook args dictionary

        # Separate label if exists for caller()
        content = args.pop("label", None)

        html = render_macro(template_path, macro_name, content=content, **args)
        return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"Render error: {str(e)}", status=500)
