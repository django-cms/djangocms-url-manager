from cms.app_base import CMSAppConfig

from djangocms_url_manager.datastructures import UrlContentItem

from .models import PollContent


class PollsCMSConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_models_support = [
        UrlContentItem(
            content_model=PollContent,
        ),
    ]
