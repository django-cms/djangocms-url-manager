from django.conf import settings

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page

from djangocms_url_manager.utils import parse_settings

from .models import Url


class UrlCMSAppConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [Page]
    djangocms_navigation_enabled = getattr(settings, "DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED", False)
    navigation_models = {Url: ["internal_name"]}


class UrlManagerCMSExtension(CMSAppExtension):
    def __init__(self):
        self.url_manager_supported_models = {}

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_supported_models settings has been correctly set
        and add it to the masterlist
        """
        self.url_manager_supported_models = parse_settings(cms_config, "url_manager_supported_models")

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
