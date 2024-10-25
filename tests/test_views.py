from unittest import skipUnless

from django.contrib.contenttypes.models import ContentType

from cms.models import User
from cms.utils.urlutils import admin_reverse

from djangocms_url_manager.constants import SELECT2_URLS
from djangocms_url_manager.test_utils.factories import UrlWithVersionFactory
from djangocms_url_manager.utils import is_versioning_enabled

from .base import BaseUrlTestCase


class UrlManagerSelect2ContentObjectViewsTestCase(BaseUrlTestCase):
    def test_select2_view_no_content_id(self):
        with self.login_user_context(self.superuser):
            with self.assertRaises(ValueError) as err:
                self.client.get(self.select2_endpoint)
            self.assertEqual(
                str(err.exception), "Content type with id None does not exists."
            )

    def test_select2_view_no_permission(self):
        response = self.client.get(self.select2_endpoint)
        self.assertEqual(response.status_code, 403)

    def test_return_page_in_select2_view(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint, data={"content_id": self.page_contenttype_id}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p["id"] for p in response.json()["results"]], [self.page.pk, self.page2.pk]
        )

    @skipUnless(BaseUrlTestCase.is_versioning_enabled(), "Test only relevant for versioning")
    def test_return_page_in_select2_view_with_versioning(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint, data={"content_id": self.page_contenttype_id}
            )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json()["results"],
            [
                {"text": self.page.get_title(), "id": self.page.pk},
                {"text": self.page2.get_title(), "id": self.page2.pk},
            ],
        )

    def test_select2_view(self):

        with self.login_user_context(self.superuser):
            response = self.client.get(
                admin_reverse(
                    SELECT2_URLS,
                ),
            )

        result = [self.url.pk, self.url2.pk, ]
        text_result = []

        if is_versioning_enabled():
            # The following versions have draft content
            text_result.append(f"{self.url.internal_name} (Not published)")
            text_result.append(f'{self.url2.internal_name} (Not published)')
        else:
            text_result.append(f"{self.url.internal_name}")
            text_result.append(f"{self.url2.internal_name}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([a['id'] for a in response.json()['results']], result)
        self.assertEqual(
            [a['text'] for a in response.json()['results']],
            text_result,
        )

    def test_return_poll_content_in_select2_view(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={"content_id": self.poll_content_contenttype_id},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p["id"] for p in response.json()["results"]],
            [self.poll_content.pk, self.poll_content2.pk],
        )

    def test_raise_error_when_return_unregistered_user_model_in_select2_view(self):
        with self.login_user_context(self.superuser):
            with self.assertRaises(ValueError):
                self.client.get(
                    self.select2_endpoint,
                    data={"content_id": ContentType.objects.get_for_model(User).id},
                )

    def test_select2_view_set_limit(self):
        self._create_page(title="test 3", language=self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={"content_id": self.page_contenttype_id, "limit": 2},
            )

        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content["more"])
        self.assertEqual(len(content["results"]), 2)

    def test_select2_view_text_page_repr(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint, data={"content_id": self.page_contenttype_id}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["text"], str(self.page))

    def test_select2_view_text_poll_content_repr(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={"content_id": self.poll_content_contenttype_id},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["text"], str(self.poll_content))

    def test_select2_view_site(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={"content_id": self.page_contenttype_id, "site": self.site2.pk},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([a["id"] for a in response.json()["results"]], [self.page2.pk])

    def test_select2_page_view_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    "content_id": self.page_contenttype_id,
                    "site": self.site2.pk,
                    "pk": self.page2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([a["id"] for a in response.json()["results"]], [self.page2.pk])

    def test_select2_poll_content_view_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    "content_id": self.poll_content_contenttype_id,
                    "site": self.site2.pk,
                    "pk": self.poll_content.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a["id"] for a in response.json()["results"]], [self.poll_content.pk]
        )


class UrlManagerSelect2UrlsViewsTestCase(BaseUrlTestCase):
    def test_select2_url_view_no_permission(self):
        response = self.client.get(self.select2_urls_endpoint)
        self.assertEqual(response.status_code, 403)

    def test_select2_url_view_without_site_id(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(self.select2_urls_endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p["id"] for p in response.json()["results"]], [self.url.pk, self.url2.pk]
        )

    def test_select2_url_view_with_site_id(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint, data={"site": self.site2.pk}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([p["id"] for p in response.json()["results"]], [self.url2.pk])

    def test_select2_url_view_with_object_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint, data={"pk": self.url2.pk}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([a["id"] for a in response.json()["results"]], [self.url2.pk])

    def test_select2_url_view_set_limit(self):
        # Create a third url so the "more" option should be True
        UrlWithVersionFactory(site=self.default_site)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.select2_urls_endpoint, data={"limit": 2})

        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content["more"])
        self.assertEqual(len(content["results"]), 2)
