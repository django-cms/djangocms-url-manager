from cms.app_base import CMSAppConfig

from .models import PollContent


class PollsCMSConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [PollContent]
