from unittest import skipUnless

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from cms.test_utils.testcases import CMSTestCase

from djangocms_url_manager.compat import CMS_36


@skipUnless(CMS_36, "CMS<4.0")
class CMSSettingsUnitTestCase(CMSTestCase):

    @override_settings()
    def test_missing_url_manager_support_models_attribute(self):
        """Tests, if the URL_MANAGER_SUPPORT_MODELS attribute has not been specified
        in settings file, an ImproperlyConfigured exception is raised
        """
        del settings._wrapped.URL_MANAGER_SUPPORTED_MODELS
        with self.assertRaises(ImproperlyConfigured):
            apps.get_app_config('djangocms_url_manager').ready()

    @override_settings(URL_MANAGER_SUPPORTED_MODELS='polls.Poll')
    def test_raises_exception_if_url_manager_models_support_is_not_list(self):
        """Tests ImproperlyConfigured exception is raised if
        URL_MANAGER_SUPPORT_MODELS setting is not a list
        """
        with self.assertRaises(ImproperlyConfigured):
            apps.get_app_config('djangocms_url_manager').ready()

    @override_settings(URL_MANAGER_SUPPORTED_MODELS=['aaa', {}])
    def test_raises_exception_if_url_manager_supported_models_item_has_not_correct_model_app_path(self):
        """Tests ValueError exception is raised if elements
        in the URL_MANAGER_SUPPORT_MODELS list are not valid model path.
        """
        with self.assertRaises(ImproperlyConfigured):
            apps.get_app_config('djangocms_url_manager').ready()

    @override_settings(URL_MANAGER_SUPPORTED_MODELS=['test.Test'])
    def test_raises_exception_if_url_manager_supported_models_item_are_not_valid_django_app(self):
        """Tests LookupError exception is raised if elements
        in the URL_MANAGER_SUPPORT_MODELS list are not valid django app.
        """
        with self.assertRaises(LookupError):
            apps.get_app_config('djangocms_url_manager').ready()

    @override_settings(URL_MANAGER_SUPPORTED_MODELS=['polls.Poll'])
    def test_raises_exception_if_url_manager_supported_models_model_does_not_have_url_method(self):
        """Tests ImproperlyConfigured exception is raised if a
        model does not have get_absolute_url implemented
        """
        with self.assertRaises(ImproperlyConfigured):
            apps.get_app_config('djangocms_url_manager').ready()
