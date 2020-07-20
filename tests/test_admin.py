from .base import BaseUrlTestCase


class UrlManagerTestCase(BaseUrlTestCase):

    def test_get_search_results(self):
        """
        Test that a filtered queryset is returned containing matches with a given search_term
        Ensure querysets are combined to prevent search from only returning the last hit!
        """
        self.url2.content_object = self.page
        self.url2.save()
        search_term = self.page.get_title()

        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.first(), self.url)
        self.assertEqual(results.last(), self.url2)
        self.assertEqual(results.count(), 2)

    def test_failed_to_find_results(self):
        """
        Test failures to find terms are handled gracefully.
        """
        search_term = "xxxxxxxxx"

        results, use_distinct = self.url_admin.get_search_results(
            self.url_admin_request, self.url_queryset, search_term
        )

        self.assertEqual(results.count(), 0)
