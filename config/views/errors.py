from django.shortcuts import render
from django.views import defaults as default_views
from django.views.generic import TemplateView


class BaseErrorView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        request = self.request
        exception = kwargs.get("exception")

        response = self.get_response(request, exception)

        context = response.context_data if hasattr(response, "context_data") else {}
        context["breadcrumbs"] = self.get_breadcrumbs()

        return context

    def get_breadcrumbs(self):
        raise NotImplementedError("Subclasses must implement this method")

    def dispatch(self, request, *args, **kwargs):
        exception = kwargs.get("exception")
        return render(
            request, self.template_name, self.get_context_data(exception=exception), status=self.get_error_status(),
        )

    def get_error_status(self):
        raise NotImplementedError("Subclasses must implement this method")


class NotFoundView(BaseErrorView):
    template_name = "404.html"

    def get_response(self, request, exception):
        return default_views.page_not_found(request, exception, self.template_name)

    def get_breadcrumbs(self):
        return [{"text": "Page not found"}]

    def get_error_status(self):
        return 404


class ServerErrorView(BaseErrorView):
    template_name = "500.html"

    def get_response(self, request, exception):
        return default_views.server_error(request, self.template_name)

    def get_breadcrumbs(self):
        return [{"text": "Server Error"}]

    def get_error_status(self):
        return 500


class PermissionDeniedView(BaseErrorView):
    template_name = "403.html"

    def get_response(self, request, exception):
        return default_views.permission_denied(request, exception, self.template_name)

    def get_breadcrumbs(self):
        return [{"text": "Forbidden"}]

    def get_error_status(self):
        return 403
