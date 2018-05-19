from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UrlManagerConfig(AppConfig):
    name = 'djangocms_url_manager'
    verbose_name = _('django CMS URL Manager')
