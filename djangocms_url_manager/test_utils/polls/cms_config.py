from cms.app_base import CMSAppConfig
from cms.models import Page

from djangocms_url_manager.utils import get_page_search_results
from .models import PollContent
from .utils import get_all_poll_content_objects, get_poll_search_results


class PollsCMSConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [Page, (PollContent, get_all_poll_content_objects)]
    url_manager_supported_models_search_helpers = {
        Page: get_page_search_results,
        PollContent: get_poll_search_results,
    }
