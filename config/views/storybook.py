import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Import your Jinja macro renderer


@csrf_exempt
def storybook_render_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Must be a POST request"}, status=405)

    try:
        data = json.loads(request.body)
        template_path = data.get("template")
        macro_name = data.get("macro")

        from storybook.render_jinja_core import render_macro

        # Only pass arguments that exist
        html_kwargs = {}
        if "label" in data:
            html_kwargs["content"] = data["label"]
        if "variant" in data:
            html_kwargs["variant"] = data["variant"]
        if "size" in data:
            html_kwargs["size"] = data["size"]

        html = render_macro(template_path, macro_name, **html_kwargs)
        return HttpResponse(html)

    except Exception:
        logging.exception("Error rendering storybook macro")
        return JsonResponse({"error": "Internal server error"}, status=500)
