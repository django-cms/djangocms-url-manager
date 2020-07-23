from unittest import skipUnless

from djangocms_url_manager.test_utils import polls

from .base import BaseUrlTestCase


class UrlManagerTestCase(BaseUrlTestCase):
    def test_get_search_results(self):
        """
        A filtered queryset is returned containing matches with a given search_term
        Ensure querysets are combined to prevent search from only returning the last hit!
        """
        self.url2.content_object = self.page2
        self.url2.save()
        print(dir(self.poll_content))
        search_term = self.page.get_title()
        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.first(), self.url)
        self.assertEqual(results.last(), self.url2)
        self.assertEqual(results.count(), 2)

    @skipUnless(
        BaseUrlTestCase.is_versioning_enabled(), "Test only relevant for versioning"
    )
    def test_get_search_results_versioning(self):
        from djangocms_versioning.constants import DRAFT
        poll_published = self.poll_content
        poll_published._publish(poll_published.poll, DRAFT, self.language)
        poll_draft = self.poll_content2


        self.url2.content_object = self.poll
        search_term = self.poll_content.text

        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.first().content_object, self.poll_published)
        self.assertEqual(results.count(), 1)

    def test_failed_to_find_results(self):
        """
        Failures to find terms should be handled gracefully.
        """
        search_term = "xxxxxxxxx"

        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.count(), 0)

    def test_get_search_results_poll_contents(self):
        app_config = polls.cms_config.PollsCMSConfig
