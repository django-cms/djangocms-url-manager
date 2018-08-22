from cms.api import add_plugin

from djangocms_url_manager.cms_plugins import HtmlLink
from djangocms_url_manager.compat import get_page_placeholders

from .base import BaseUrlManagerPluginTestCase


class UrlManagerPluginTestCase(BaseUrlManagerPluginTestCase):

    def test_get_render_template(self):
        placeholder = get_page_placeholders(
            self.page,
            self.language,
        ).get(slot='content')

        plugin = add_plugin(
            placeholder,
            'HtmlLink',
            language=self.language,
            url=self.url,
            label='Test URL plugin',
        )

        self.assertEqual(
            HtmlLink().get_render_template({}, plugin, placeholder),
            'djangocms_url_manager/default/url.html',
        )
