from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import LinkPlugin


__all__ = [
    'HtmlLink',
]


@plugin_pool.register_plugin
class HtmlLink(CMSPluginBase):
    name = _('Link')
    model = LinkPlugin

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_url_manager/{}/url.html'.format(instance.template)
