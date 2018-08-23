from cms.api import create_page

from .base import BaseUrlManagerPluginTestCase


class UrlManagerViewsTestCase(BaseUrlManagerPluginTestCase):

    def test_select2_view_no_permission(self):
        response = self.client.get(self.select2_endpoint)
        self.assertEqual(response.status_code, 403)

    def test_select2_view(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(self.select2_endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [p['id'] for p in response.json()['results']],
            [self.page.pk, self.page2.pk],
        )

    def test_select2_view_set_limit(self):
        create_page(
            title='test 3',
            template='page.html',
            language=self.language,
            in_navigation=True,
        )
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'limit': 2},
            )

        content = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['more'])
        self.assertEqual(len(content['results']), 2)

    def test_select2_view_text_repr(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(self.select2_endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'][0]['text'],
            str(self.page),
        )

    def test_select2_view_term(self):
        create_page(
            title='foo',
            template='page.html',
            language=self.language,
            in_navigation=True,
        )
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'term': 'test'},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.page.pk, self.page2.pk],
        )

    def test_select2_view_site(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'site': self.site2.pk},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.page2.pk],
        )

    def test_select2_view_pk(self):
        with self.login_user_context(self.superuser):
            response = self.client.get(
                self.select2_endpoint,
                data={'pk': self.page2.pk},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [a['id'] for a in response.json()['results']],
            [self.page2.pk],
        )
