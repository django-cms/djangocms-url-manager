from cms.app_base import CMSAppExtension

from djangocms_url_manager.utils import validate_settings


class UrlManagerCMSExtension(CMSAppExtension):

    def __init__(self):
        self.url_manager_supported_models = []

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_supported_models settings has been correctly set
        and add it to the masterlist
        """
        validate_settings(cms_config, 'url_manager_supported_models')
        self.url_manager_supported_models.extend(cms_config.url_manager_supported_models)

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
