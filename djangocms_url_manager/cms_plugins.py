from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import UrlPlugin


__all__ = [
    'Url',
]


@plugin_pool.register_plugin
class Url(CMSPluginBase):
    name = _('URL')
    model = UrlPlugin

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_url_manager/{}/url.html'.format(instance.template)
