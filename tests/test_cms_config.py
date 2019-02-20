from importlib import reload
from django.conf import settings
from unittest import skipIf
from unittest.mock import Mock


from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from cms.models import Page
from cms.test_utils.testcases import CMSTestCase


from djangocms_url_manager.compat import CMS_36
from djangocms_url_manager.test_utils.polls.models import Poll, PollContent
from djangocms_url_manager.test_utils.polls.utils import get_all_poll_content_objects
from djangocms_url_manager.utils import supported_models


@skipIf(CMS_36, "Test relevant only for CMS>=4.0")
class UrlManagerCMSExtensionTestCase(CMSTestCase):
    def test_missing_cms_config_url_manager_supported_models_attribute(self):
        """Tests, if the url_manager_supported_models attribute has not been specified,
        an ImproperlyConfigured exception is raised
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True)
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_is_not_list(self):
        """Tests ImproperlyConfigured exception is raised if
        url_manager_supported_models setting is not a list
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=PollContent)
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_item_is_not_model_class(self):
        """Tests ImproperlyConfigured exception is raised if elements
        in the url_manager_supported_models list are not valid django models class.
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=["aaa", {}])
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_model_does_not_have_url_method(self):
        """Tests ImproperlyConfigured exception is raised if a
        model does not have get_absolute_url implemented
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=[Poll])
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_emit_warning_when_duplicated_models(self):
        """Tests if Warning is emitted when in cms_config
        url_manager_supported_models are duplicated models
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=[PollContent, PollContent]
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_url_manager_supported_model(self):
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=[PollContent])
        extensions.handle_url_manager_setting(cms_config)
        self.assertDictEqual(supported_models(), {Page: None, PollContent: get_all_poll_content_objects})

    def test_url_manager_supported_tuple_model_without_function(self):
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension

        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[], djangocms_url_manager_enabled=True, url_manager_supported_models=[(PollContent)])
        extensions.handle_url_manager_setting(cms_config)
        self.assertDictEqual(supported_models(), {Page: None, PollContent: get_all_poll_content_objects})


@skipIf(CMS_36, "Test relevant only for CMS>=4.0")
class NavigationSettingTestCase(TestCase):
    def tearDownClass():
        from djangocms_url_manager import cms_config

        reload(cms_config)

    @override_settings(DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED=False)
    def test_references_setting_affects_cms_config_false(self):
        from djangocms_url_manager import cms_config

        reload(cms_config)
        self.assertFalse(cms_config.UrlCMSAppConfig.djangocms_navigation_enabled)

    @override_settings(DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED=True)
    def test_references_setting_affects_cms_config_true(self):
        from djangocms_url_manager import cms_config

        reload(cms_config)
        self.assertTrue(cms_config.UrlCMSAppConfig.djangocms_navigation_enabled)

    @override_settings()
    def test_references_setting_affects_cms_config_default(self):
        from djangocms_url_manager import cms_config

        del settings.DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED
        reload(cms_config)
        self.assertFalse(cms_config.UrlCMSAppConfig.djangocms_navigation_enabled)
