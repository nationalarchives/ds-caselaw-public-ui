from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ds_judgements_public_ui.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import ds_judgements_public_ui.users.signals  # noqa F401
        except ImportError:
            pass
