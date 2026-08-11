from functools import wraps

from django.urls import reverse


def jinja_url(name, *args, **kwargs):
    return reverse(name, args=args or None, kwargs=kwargs or None)


def with_context(fn):
    """
    Wraps a Django template tag function that takes context, so it works in Jinja.
    Assumes `request` is in the Jinja template globals.
    """

    @wraps(fn)
    def wrapped(request, *args, **kwargs):
        context = {"request": request}
        return fn(context, *args, **kwargs)

    return wrapped
