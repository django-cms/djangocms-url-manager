from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UrlManagerConfig(AppConfig):
    name = "djangocms_url_manager"
    verbose_name = _("django CMS URL Manager")
    url_manager_supported_models = {}

    def ready(self):
        from .compat import CMS_36

        if CMS_36:
            from .utils import parse_settings

            self.url_manager_supported_models = parse_settings(settings, "URL_MANAGER_SUPPORTED_MODELS")
