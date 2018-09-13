from unittest import skipIf
from unittest.mock import Mock

from django.core.exceptions import ImproperlyConfigured

from cms.test_utils.testcases import CMSTestCase

from djangocms_url_manager.compat import CMS_36
from djangocms_url_manager.test_utils.polls.models import Poll, PollContent


@skipIf(CMS_36, "Test relevant only for CMS>=4.0")
class UrlManagerCMSExtensionTestCase(CMSTestCase):

    def test_missing_cms_config_url_manager_supported_models_attribute(self):
        """Tests, if the url_manager_supported_models attribute has not been specified,
        an ImproperlyConfigured exception is raised
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_is_not_list(self):
        """Tests ImproperlyConfigured exception is raised if
        url_manager_supported_models setting is not a list
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_supported_models=PollContent
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_item_is_not_model_class(self):
        """Tests ImproperlyConfigured exception is raised if elements
        in the url_manager_supported_models list are not valid django models class.
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_supported_models=['aaa', {}]
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_supported_models_model_does_not_have_url_method(self):
        """Tests ImproperlyConfigured exception is raised if a
        model does not have get_absolute_url implemented
        """
        from djangocms_url_manager.cms_config import UrlManagerCMSExtension
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_supported_models=[Poll]
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)
