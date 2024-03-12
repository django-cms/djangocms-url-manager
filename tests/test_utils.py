from cms.models import Page, Placeholder

from djangocms_url_manager.test_utils.polls.models import PollContent
from djangocms_url_manager.test_utils.polls.utils import get_all_poll_content_objects
from djangocms_url_manager.utils import is_model_supported, supported_models

from .base import BaseUrlTestCase


class UtilsTestCase(BaseUrlTestCase):

    def test_supported_models_for_cms40(self):
        self.assertDictEqual(
            supported_models(), {Page: None, PollContent: get_all_poll_content_objects}
        )

    def test_is_model_available_method_for_cms40(self):
        self.assertTrue(is_model_supported(PollContent))
        self.assertTrue(is_model_supported(Page))
        self.assertFalse(is_model_supported(Placeholder))
