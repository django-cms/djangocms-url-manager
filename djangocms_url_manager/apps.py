from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UrlManagerConfig(AppConfig):
    name = 'djangocms_url_manager'
    verbose_name = _('django CMS URL Manager')

    def ready(self):
        from .compat import CMS_36

        if CMS_36:
            from .utils import validate_settings
            validate_settings(settings, 'URL_MANAGER_SUPPORTED_MODELS')
