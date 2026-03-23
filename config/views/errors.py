from django.views.generic import TemplateView


class BaseErrorView(TemplateView):
    template_name = None
    template_engine = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        raise NotImplementedError

    def get_error_status(self):
        raise NotImplementedError

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", self.get_error_status())
        return super().render_to_response(context, **response_kwargs)


class NotFoundView(BaseErrorView):
    template_engine = "jinja"
    template_name = "404.jinja"

    def get_breadcrumbs(self):
        return [{"text": "Page not found"}]

    def get_error_status(self):
        return 404


class ServerErrorView(BaseErrorView):
    template_engine = "jinja"
    template_name = "500.jinja"

    def get_breadcrumbs(self):
        return [{"text": "Server Error"}]

    def get_error_status(self):
        return 500


class PermissionDeniedView(BaseErrorView):
    template_engine = "jinja"
    template_name = "403.jinja"

    def get_breadcrumbs(self):
        return [{"text": "Forbidden"}]

    def get_error_status(self):
        return 403
