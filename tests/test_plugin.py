from cms.api import add_plugin

from djangocms_url_manager.cms_plugins import Url

from .base import BaseUrlManagerPluginTestCase


class UrlManagerPluginTestCase(BaseUrlManagerPluginTestCase):

    def test_get_render_template(self):
        placeholder = self.page.get_placeholders(self.language).get(
            slot='content'
        )
        plugin = add_plugin(
            placeholder,
            'Url',
            language=self.language,
            url=self.url,
            name='Test URL plugin',
        )

        self.assertEqual(
            Url().get_render_template({}, plugin, placeholder),
            'djangocms_url_manager/default/url.html',
        )
