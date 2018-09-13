from unittest import skipIf, skipUnless

from django.test import override_settings

from cms.models import Page, Placeholder

from djangocms_url_manager.compat import CMS_36
from djangocms_url_manager.test_utils.polls.models import PollContent
from djangocms_url_manager.utils import is_model_supported, supported_models

from .base import BaseUrlTestCase


class UtilsTestCase(BaseUrlTestCase):

    def test_supported_models(self):
        expected_models = [Page, PollContent]
        self.assertEqual(len(supported_models()), len(expected_models))
        self.assertTrue(all(model in expected_models for model in supported_models()))

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    @override_settings(URL_MANAGER_SUPPORTED_MODELS=['polls.PollContent'])
    def test_is_model_available_method_for_cms36(self):
        self.assertTrue(is_model_supported(PollContent))
        self.assertFalse(is_model_supported(Page))

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_is_model_available_method_for_cms40(self):
        self.assertTrue(is_model_supported(PollContent))
        self.assertTrue(is_model_supported(Page))
        self.assertFalse(is_model_supported(Placeholder))
