from cms.app_base import CMSAppConfig

from .models import BlogContent


class BlogpostCMSConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [
        BlogContent,
    ]
