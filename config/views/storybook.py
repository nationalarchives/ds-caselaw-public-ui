import json
import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Import your Jinja macro renderer

logger = logging.getLogger(__name__)


def _add_storybook_cors_headers(request, response):
    origin = request.headers.get("Origin")
    if origin in settings.STORYBOOK_CORS_ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Vary"] = "Origin"
    return response


@csrf_exempt
def storybook_render_view(request):
    if request.method == "OPTIONS":
        return _add_storybook_cors_headers(request, HttpResponse())

    if request.method != "POST":
        response = JsonResponse({"error": "Must be a POST request"}, status=405)
        return _add_storybook_cors_headers(request, response)

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
        return _add_storybook_cors_headers(request, HttpResponse(html))

    except Exception:
        logger.exception("Error rendering storybook macro")
        response = JsonResponse({"error": "Internal server error"}, status=500)
        return _add_storybook_cors_headers(request, response)
