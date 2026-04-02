from django.utils.text import slugify

BASE_TRACKING_CLASS = "analytics"


def trackable_class_name(text):
    return f"{BASE_TRACKING_CLASS}-{slugify(text)}"


def trackable_link(context, text, **attrs):
    request = context.get("request")

    current_path = request.path if request else ""

    class_name = trackable_class_name(text)

    return {"text": text, "attrs": attrs, "class_name": class_name, "current_path": current_path}
