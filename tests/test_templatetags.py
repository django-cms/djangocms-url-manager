from urllib.parse import urlparse

from django.test import override_settings

from djangocms_versioning.constants import PUBLISHED

from djangocms_url_manager.test_utils.factories import UrlOverrideFactory, UrlVersionFactory

from .base import BaseUrlTestCase


class UrlManagerTemplateTagsTestCase(BaseUrlTestCase):
    url_template = (
        """{% load djangocms_url_manager_tags %}{% render_url url.url_grouper %}"""
    )  # noqa: E501

    def test_render_url(self):
        url_version = UrlVersionFactory(
            content__site=self.default_site,
            content__content_object=self.page,
            state=PUBLISHED,
        )

        output = self.render_template_obj(
            self.url_template, {"url": url_version.content}, self.get_request("/")
        )
        parsed = urlparse(output)

        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_render_url_other_site(self):
        url_version = UrlVersionFactory(
            content__site=self.default_site,
            content__content_object=self.page2,
            state=PUBLISHED,
        )
        UrlOverrideFactory(
            url=url_version.content,
            site=self.site2,
            content_object=self.page2,
        )

        with override_settings(SITE_ID=self.site2.pk):
            output = self.render_template_obj(
                self.url_template, {"url": url_version.content}, self.get_request("/")
            )

        parsed = urlparse(output)

        self.assertEqual(parsed.netloc, "foo.com")
        self.assertEqual(parsed.path, "/en/test2/")
