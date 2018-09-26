from unittest import skipIf, skipUnless

from django.contrib.contenttypes.models import ContentType

from cms.api import create_page
from cms.models import Page, User

from djangocms_url_manager.compat import CMS_36

from .base import BaseUrlTestCase


class UrlManagerSelect2ContentObjectViewsTestCase(BaseUrlTestCase):

    def test_select2_view_no_content_id(self):
        with self.login_user_context(self.superuser):
            with self.assertRaises(ValueError) as err:
                self.client.get(self.select2_endpoint)
            self.assertEqual(
                str(err.exception),
                'Content type with id None does not exists.'
            )

    def test_select2_view_no_permission(self):
        response = self.client.get(self.select2_endpoint)
        self.assertEqual(response.status_code, 403)

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    def test_return_page_in_select2_view_for_cms36(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.page_contenttype_id,
                    'site': self.site2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [Page.objects.published(self.site2.pk).filter(publisher_is_draft=False).last().pk],
        )

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_return_page_in_select2_view_for_cms40(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.page_contenttype_id},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [self.page.pk, self.page2.pk],
        )

    def test_return_poll_content_in_select2_view(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.poll_content_contenttype_id},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [self.poll_content.pk, self.poll_content2.pk],
        )

    def test_raise_error_when_return_unregistered_user_model_in_select2_view(self):
        with self.login_user_context(self.superuser):
            with self.assertRaises(ValueError):
                self.client.get(
                    self.select2_endpoint,
                    data={'content_id': ContentType.objects.get_for_model(User).id},
                )

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    def test_select2_view_set_limit_for_cms36(self):
        create_page(
            title='test 3',
            template='page.html',
            language=self.language,
            in_navigation=True,
            published=True,
        )
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.page_contenttype_id, 'limit': 1},
            )

        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['more'])
        self.assertEqual(len(content['results']), 1)

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_select2_view_set_limit_for_cms40(self):
        create_page(
            title='test 3',
            template='page.html',
            language=self.language,
            in_navigation=True,
        )
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.page_contenttype_id, 'limit': 2},
            )

        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['more'])
        self.assertEqual(len(content['results']), 2)

    def test_select2_view_text_page_repr(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.page_contenttype_id},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'][0]['text'],
            str(self.page),
        )

    def test_select2_view_text_poll_content_repr(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'content_id': self.poll_content_contenttype_id},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'][0]['text'],
            str(self.poll_content),
        )

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    def test_select2_view_site_for_cms36(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.page_contenttype_id,
                    'site': self.site2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [Page.objects.published(self.site2.pk).filter(publisher_is_draft=False).last().pk],
        )

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_select2_view_site_for_cms40(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.page_contenttype_id,
                    'site': self.site2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.page2.pk],
        )

    @skipUnless(CMS_36, "Test relevant only for CMS<4.0")
    def test_select2_page_view_pk_for_cms36(self):
        page = Page.objects.published(self.site2.pk).filter(publisher_is_draft=False).last().pk
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.page_contenttype_id,
                    'site': self.site2.pk,
                    'pk': page,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [page],
        )

    @skipIf(CMS_36, "Test relevant only for CMS>=4.0")
    def test_select2_page_view_pk_for_cms40(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.page_contenttype_id,
                    'site': self.site2.pk,
                    'pk': self.page2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.page2.pk],
        )

    def test_select2_poll_content_view_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={
                    'content_id': self.poll_content_contenttype_id,
                    'site': self.site2.pk,
                    'pk': self.poll_content.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.poll_content.pk],
        )


class UrlManagerSelect2UrlsViewsTestCase(BaseUrlTestCase):

    def test_select2_url_view_no_permission(self):
        response = self.client.get(self.select2_urls_endpoint)
        self.assertEqual(response.status_code, 403)

    def test_select2_url_view_without_site_id(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [self.url.pk, self.url2.pk],
        )

    def test_select2_url_view_with_site_id(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint,
                data={
                    'site': self.site2.pk,
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [self.url2.pk],
        )

    def test_select2_url_view_with_object_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint,
                data={
                    'pk': self.url2.pk,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.url2.pk],
        )

    def test_select2_url_view_set_limit(self):
        self._create_url(anchor='test')
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_urls_endpoint,
                data={
                    'limit': 2,
                },
            )
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['more'])
        self.assertEqual(len(content['results']), 2)
