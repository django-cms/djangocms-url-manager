from unittest.mock import Mock

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from cms.test_utils.testcases import CMSTestCase

from djangocms_url_manager.cms_config import UrlManagerCMSExtension
from djangocms_url_manager.datastructures import UrlContentItem
from djangocms_url_manager.test_utils.blogpost.models import BlogContent
from djangocms_url_manager.test_utils.polls.models import PollContent


class CMSConfigUnitTestCase(CMSTestCase):

    def test_missing_cms_config_url_manager_models_support_attribute(self):
        """Tests, if the url_manager_models_support attribute has not been specified,
        an ImproperlyConfigured exception is raised
        """
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[],
                          djangocms_url_manager_enabled=True)

        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_url_manager_models_support_not_iterable(self):
        """Tests ImproperlyConfigured exception is raised if
        url_manager_models_support setting is not an iterable
        """
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            versioning=UrlContentItem(
                content_model=PollContent
            )
        )
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_raises_exception_if_not_url_content_item_class(self):
        """Tests ImproperlyConfigured exception is raised if elements
        in the url_manager_models_support list are not instances of UrlContentItem class.
        """
        extensions = UrlManagerCMSExtension()
        cms_config = Mock(spec=[],
                          djangocms_url_manager_enabled=True,
                          url_manager_models_support=['aaa', {}])
        with self.assertRaises(ImproperlyConfigured):
            extensions.handle_url_manager_setting(cms_config)

    def test_url_support_content_types_models_list_created(self):
        """Test handle_url_manager_setting method adds all the
        models into the url_support_content_types_models list
        """
        extension = UrlManagerCMSExtension()
        poll_content_type_item = UrlContentItem(content_model=PollContent)
        blog_content_type_item = UrlContentItem(content_model=BlogContent)
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_models_support=[poll_content_type_item, blog_content_type_item]
        )
        extension.handle_url_manager_setting(cms_config)
        self.assertListEqual(
            extension.url_support_content_types_models, [poll_content_type_item, blog_content_type_item])

    def test_is_content_model_versioned(self):
        """Test that is_content_model_versioned returns True for
        content model that's versioned
        """
        extension = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_models_support=[UrlContentItem(content_model=PollContent)]
        )
        extension.handle_url_manager_setting(cms_config)
        self.assertTrue(extension.is_content_model_enabled(PollContent))

    def test_is_content_model_not_versioned(self):
        """Test that is_content_model_versioned returns False for
        content model that's not versioned
        """
        extension = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_models_support=[]
        )
        extension.handle_url_manager_setting(cms_config)
        self.assertFalse(extension.is_content_model_enabled(PollContent))

    def test_get_content_types_queryset_return_filtered_queryset(self):
        """Test get_content_types_queryset returns queryset containing
        records based on url_support_content_types_models list.
        """
        extension = UrlManagerCMSExtension()
        poll_content_type_item = UrlContentItem(content_model=PollContent)
        blog_content_type_item = UrlContentItem(content_model=BlogContent)
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_models_support=[poll_content_type_item, blog_content_type_item]
        )
        extension.handle_url_manager_setting(cms_config)

        self.assertQuerysetEqual(
            extension.get_content_types_queryset(),
            ContentType.objects.filter(id__in=[
                ContentType.objects.get_for_model(poll_content_type_item.content_model).id,
                ContentType.objects.get_for_model(blog_content_type_item.content_model).id,
            ]),
            transform=lambda x: x, ordered=False)

    def test_get_content_types_queryset_return_empty_queryset(self):
        """Test get_content_types_queryset returns empty queryset."""
        extension = UrlManagerCMSExtension()
        cms_config = Mock(
            spec=[],
            djangocms_url_manager_enabled=True,
            url_manager_models_support=[]
        )
        extension.handle_url_manager_setting(cms_config)

        self.assertQuerysetEqual(
            extension.get_content_types_queryset(),
            ContentType.objects.filter(id__in=[]),
            transform=lambda x: x, ordered=False)
