import warnings

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page

from djangocms_url_manager.utils import validate_settings


class UrlCMSAppConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [Page]


class UrlManagerCMSExtension(CMSAppExtension):

    def __init__(self):
        self.url_manager_supported_models = []

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_supported_models settings has been correctly set
        and add it to the masterlist
        """
        validate_settings(cms_config, 'url_manager_supported_models')
        for model in cms_config.url_manager_supported_models:
            if model in self.url_manager_supported_models:
                warnings.warn(
                    'Model {!r} is duplicated in url_manager_supported_models'.format(model),
                    UserWarning,
                )
            else:
                self.url_manager_supported_models.append(model)

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
