from unittest import skipIf, skipUnless

from django.apps import apps
from django.test import override_settings

from cms.models import Page, Placeholder

from djangocms_url_manager.compat import CMS_36
from djangocms_url_manager.test_utils.polls.models import PollContent
from djangocms_url_manager.test_utils.polls.utils import get_all_poll_content_objects, get_published_pages_objects
from djangocms_url_manager.utils import is_model_supported, supported_models

from .base import BaseUrlTestCase


class UtilsTestCase(BaseUrlTestCase):
    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    def test_supported_models_for_cms36(self):
        apps.get_app_config("djangocms_url_manager").ready()
        self.assertDictEqual(
            supported_models(), {Page: get_published_pages_objects, PollContent: get_all_poll_content_objects}
        )

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_supported_models_for_cms40(self):
        self.assertDictEqual(supported_models(), {Page: None, PollContent: get_all_poll_content_objects})

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    @override_settings(
        URL_MANAGER_SUPPORTED_MODELS=[
            ("cms.Page", get_published_pages_objects),
            ("polls.PollContent", get_all_poll_content_objects),
        ]
    )
    def test_is_model_available_method_for_cms36(self):
        apps.get_app_config("djangocms_url_manager").ready()
        self.assertTrue(is_model_supported(PollContent))
        self.assertTrue(is_model_supported(Page))
        self.assertFalse(is_model_supported(Placeholder))

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_is_model_available_method_for_cms40(self):
        self.assertTrue(is_model_supported(PollContent))
        self.assertTrue(is_model_supported(Page))
        self.assertFalse(is_model_supported(Placeholder))
