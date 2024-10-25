from unittest import skipUnless

from django.shortcuts import reverse

from djangocms_url_manager.test_utils.factories import (
    UrlFactory,
)
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


class UrlAdminChangeListViewTestCase(BaseUrlTestCase):
    
    @skipUnless(
        BaseUrlTestCase.is_versioning_enabled(), "Test only relevant if versioning enabled."
    )
    def test_get_burger_menu_on_changelist_view(self):
        """
        Verify that burger menu exists in actions column on changelist view.
        With the exception of preview & edit actions, a burger menu should be created for
        all changelist actions if UrlAdmin has inherited from ExtendedVersionAdminMixin.
        """
        
        # Move this to a setup routine if more than one function uses it.
        self.client.force_login(self.superuser)

        # Import directly into function as only used here.
        from bs4 import BeautifulSoup

        list_url = reverse(
            "admin:djangocms_url_manager_url_changelist"
        )
        response = self.client.get(list_url)

        # Parse returned html:
        soup = BeautifulSoup(str(response.content, response.charset), features="lxml")
        # Assert / verify find_all() does not return an empty string:
        self.assertTrue(soup.find_all("a", class_="cms-versioning-action-btn"))
