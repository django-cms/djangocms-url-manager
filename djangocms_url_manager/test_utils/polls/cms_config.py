from cms.app_base import CMSAppConfig
from cms.models import Page

from .models import PollContent
from .utils import get_all_poll_content_objects


class PollsCMSConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [Page, (PollContent, get_all_poll_content_objects)]
