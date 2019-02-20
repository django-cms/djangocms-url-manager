from urllib.parse import urlparse

from django.contrib.sites.models import Site

from cms.api import add_plugin

from djangocms_url_manager.compat import get_page_placeholders

from .base import BaseUrlTestCase


class UrlManagerModelsTestCase(BaseUrlTestCase):
    def test__get_url_obj(self):
        self.assertEqual(self.url._get_url_obj(self.url.site), self.url)

    def test__get_url_obj_other_site(self):
        urloverride = self._create_url_override(self.url, self.site2, self.page2)
        self.assertEqual(self.url._get_url_obj(self.site2), urloverride)

    def test__get_url_obj_other_site_with_no_override(self):
        site3 = Site.objects.create(name="bar.com", domain="bar.com")
        self.assertEqual(self.url._get_url_obj(site3), self.url)

    def test_get_url_page(self):
        url = self._create_url(content_object=self.page)
        parsed = urlparse(url.get_url(url.site))
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_get_url_manual_url(self):
        url = self._create_url(manual_url="https://google.com")
        self.assertEqual(url.get_url(url.site), "https://google.com")

    def test_get_absolute_url_page(self):
        url = self._create_url(content_object=self.page)
        parsed = urlparse(url.get_absolute_url())
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_str_page(self):
        url = self._create_url(content_object=self.page)
        parsed = urlparse(str(url))
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_get_absolute_url_manual_url(self):
        url = self._create_url(manual_url="https://google.com")
        self.assertEqual(url.get_absolute_url(), "https://google.com")

    def test_str_manual_url(self):
        url = self._create_url(manual_url="https://google.com")
        self.assertEqual(str(url), "https://google.com")

    def test_get_absolute_url_phone(self):
        url = self._create_url(phone="555555555")
        self.assertEqual(url.get_absolute_url(), "tel:555555555")

    def test_str_phone(self):
        url = self._create_url(phone="555555555")
        self.assertEqual(str(url), "tel:555555555")

    def test_get_absolute_url_mailto(self):
        url = self._create_url(mailto="test@example.com")
        self.assertEqual(url.get_absolute_url(), "mailto:test@example.com")

    def test_str_mailto(self):
        url = self._create_url(mailto="test@example.com")
        self.assertEqual(str(url), "mailto:test@example.com")

    def test_get_absolute_url_anchor(self):
        url = self._create_url(anchor="foo")
        self.assertEqual(url.get_absolute_url(), "#foo")

    def test_str_anchor(self):
        url = self._create_url(anchor="foo")
        self.assertEqual(str(url), "#foo")

    def test_get_url_phone(self):
        url = self._create_url(phone="555555555")
        self.assertEqual(url.get_url(url.site), "tel:555555555")

    def test_get_url_mailto(self):
        url = self._create_url(mailto="test@example.com")
        self.assertEqual(url.get_url(url.site), "mailto:test@example.com")

    def test_get_url_no_data(self):
        url = self._create_url()
        self.assertEqual(url.get_url(url.site), "")

    def test_get_url_anchor(self):
        url = self._create_url(anchor="foo")
        self.assertEqual(url.get_url(url.site), "#foo")

    def test_get_url_page_combined_with_anchor(self):
        url = self._create_url(content_object=self.page, anchor="foo")
        parsed = urlparse(url.get_url(url.site))
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")
        self.assertEqual(parsed.fragment, "foo")

    def test_get_url_phone_not_combined_with_anchor(self):
        url = self._create_url(phone="555555555", anchor="foo")
        self.assertEqual(url.get_url(url.site), "tel:555555555")

    def test_get_url_phone_shadows_mailto(self):
        url = self._create_url(phone="555555555", mailto="test@example.com", anchor="foo")
        self.assertEqual(url.get_url(url.site), "tel:555555555")

    def test_get_url_manual_url_shadows_phone_and_mailto(self):
        url = self._create_url(manual_url="https://google.com", phone="555555555", anchor="foo")
        self.assertEqual(url.get_url(url.site), "https://google.com")

    def test_get_url_page_shadows_manual_url_phone_and_mailto(self):
        url = self._create_url(content_object=self.page, manual_url="https://google.com", anchor="foo")
        parsed = urlparse(url.get_url(url.site))
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")
        self.assertEqual(parsed.fragment, "foo")

    def test_url_str(self):
        self.assertEqual(str(self.url), "//example.com/en/test/")

    def test_urlplugin_str(self):
        placeholder = get_page_placeholders(self.page, self.language).get(slot="content")
        plugin = add_plugin(placeholder, "HtmlLink", language=self.language, url=self.url, label="Test URL plugin")
        self.assertEqual(str(plugin), plugin.label)
