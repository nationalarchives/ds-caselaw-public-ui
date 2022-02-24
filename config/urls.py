from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "open-justice-licence",
        TemplateView.as_view(template_name="pages/open_justice_licence.html"),
        name="open_justice_licence",
    ),
    path(
        "terms-of-use",
        TemplateView.as_view(template_name="pages/terms_of_use.html"),
        name="terms_of_use",
    ),
    path(
        "sources",
        TemplateView.as_view(template_name="pages/sources.html"),
        name="sources",
    ),
    path(
        "structured_search",
        TemplateView.as_view(template_name="pages/structured_search.html"),
        name="structured_search",
    ),
    path(
        "no_results",
        TemplateView.as_view(template_name="pages/no_results.html"),
        name="no_results",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path("", include("judgments.urls")),
    path("judgments_admin/", include("judgments_admin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
