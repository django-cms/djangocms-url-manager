from django.core.exceptions import ImproperlyConfigured

from cms.test_utils.testcases import CMSTestCase

from djangocms_url_manager.datastructures import UrlContentItem
from djangocms_url_manager.test_utils.polls.models import Poll


class UrlContentItemTestCase(CMSTestCase):

    def test_raises_exception_if_content_model_does_not_have_url_method(self):
        """Tests ImproperlyConfigured exception is raised if a content
        model does not have get_absolute_url implemented
        """
        # NOTE: Answer doesn't have get_absolute_url so this should
        # throw an exception
        with self.assertRaises(ImproperlyConfigured):
            UrlContentItem(content_model=Poll)
