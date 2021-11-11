from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page

from djangocms_url_manager.utils import get_page_search_results, parse_settings

from .models import Url


class UrlCMSAppConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    djangocms_versioning_enabled = True
    url_manager_supported_models = [Page]
    djangocms_navigation_enabled = getattr(
        settings, "DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED", False
    )
    navigation_models = {Url: ["internal_name"]}

    url_manager_supported_models_search_helpers = {
        Page: get_page_search_results,
    }


class UrlManagerCMSExtension(CMSAppExtension):
    def __init__(self):
        self.url_manager_supported_models = {}
        self.url_manager_supported_models_search_helpers = {}

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_supported_models settings has been correctly set
        and add it to the masterlist
        """
        self.url_manager_supported_models = parse_settings(
            cms_config, "url_manager_supported_models"
        )

    def handle_url_manager_search_setting(self, cms_config):
        """Check the handle_url_manager_search_setting settings has been correctly set
        and add it to the masterlist
        """
        if hasattr(cms_config, "url_manager_supported_models_search_helpers"):
            url_manager_model_helpers = getattr(cms_config, "url_manager_supported_models_search_helpers")
            if isinstance(url_manager_model_helpers, dict):
                self.url_manager_supported_models_search_helpers = {
                    **self.url_manager_supported_models_search_helpers, **url_manager_model_helpers
                }
            else:
                raise ImproperlyConfigured(
                    "url helpers configuration must be a dict object"
                )
        else:
            raise ImproperlyConfigured(
                "cms_config.py must have url_manager_supported_models_search_helpers attribute"
            )

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
        self.handle_url_manager_search_setting(cms_config)
