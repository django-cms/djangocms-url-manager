from unittest import skipUnless

from .base import BaseUrlTestCase


class UrlManagerContentTypeSearchTestCase(BaseUrlTestCase):

    def test_get_search_results(self):
        """
        A filtered queryset is returned containing matches with a given search_term
        Ensure querysets are combined to prevent search from only returning the last hit!
        """
        self.url2.content_object = self.page2
        self.url2.save()

        search_term = self.page.get_title()
        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.first(), self.url)
        self.assertEqual(results.last(), self.url2)
        self.assertEqual(results.count(), 2)

    def test_get_search_results_partial_search_term(self):
        """
        A filtered queryset is returned containing matches with a given search_term
        Ensure querysets are combined to prevent search from only returning the last hit and that values are returned
        for partial search terms
        """
        self.url2.content_object = self.page2
        self.url2.save()

        search_term = self.page.get_title()[:2]
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
        from djangocms_versioning.constants import DRAFT, PUBLISHED

        self._get_version(self.page, PUBLISHED, self.language)
        self._get_version(self.page, DRAFT, self.language)

        self.url.content_object = self.page
        search_term = self.page.get_title()

        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.first(), self.url)
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
