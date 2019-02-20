from cms.api import add_plugin

from djangocms_url_manager.cms_plugins import HtmlLink
from djangocms_url_manager.compat import get_page_placeholders

from .base import BaseUrlTestCase


class UrlManagerPluginTestCase(BaseUrlTestCase):
    def test_get_render_template(self):
        placeholder = get_page_placeholders(self.page, self.language).get(slot="content")

        plugin = add_plugin(placeholder, "HtmlLink", language=self.language, url=self.url, label="Test URL plugin")

        self.assertEqual(
            HtmlLink().get_render_template({}, plugin, placeholder), "djangocms_url_manager/default/url.html"
        )

    def test_default_template_show_label_when_no_children_plugins(self):
        placeholder = get_page_placeholders(self.page, self.language).get(slot="content")

        add_plugin(placeholder, "HtmlLink", language=self.language, url=self.url, label="Test URL plugin")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.page.get_absolute_url())

        self.assertContains(response, "Test URL plugin")

    def test_default_template_show_children_plugins(self):
        placeholder = get_page_placeholders(self.page, self.language).get(slot="content")

        plugin = add_plugin(placeholder, "HtmlLink", language=self.language, url=self.url, label="Test URL plugin")
        add_plugin(placeholder, "TextPlugin", language=self.language, target=plugin, body="Children plugin 1")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.page.get_absolute_url())

        self.assertNotContains(response, "Test URL plugin")
        self.assertContains(response, "Children plugin 1")
