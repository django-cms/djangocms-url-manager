from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UrlManagerConfig(AppConfig):
    name = "djangocms_url_manager"
    verbose_name = _("django CMS URL Manager")
    url_manager_supported_models = {}
