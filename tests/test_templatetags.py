from urllib.parse import urlparse

from django.test import override_settings

from .base import BaseUrlTestCase


class UrlManagerTemplateTagsTestCase(BaseUrlTestCase):
    url_template = """{% load djangocms_url_manager_tags %}{% render_url url %}"""  # noqa: E501

    def test_render_url(self):
        output = self.render_template_obj(self.url_template, {"url": self.url}, self.get_request("/"))
        parsed = urlparse(output)
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_render_url_other_site(self):
        self._create_url_override(self.url, self.site2, self.page2)
        with override_settings(SITE_ID=self.site2.pk):
            output = self.render_template_obj(self.url_template, {"url": self.url}, self.get_request("/"))
        parsed = urlparse(output)
        self.assertEqual(parsed.netloc, "foo.com")
        self.assertEqual(parsed.path, "/en/test2/")
