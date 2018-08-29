import collections

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property

from cms.app_base import CMSAppExtension

from djangocms_url_manager.datastructures import UrlContentItem


class UrlManagerCMSExtension(CMSAppExtension):

    def __init__(self):
        self.url_support_content_types_models = []

    def get_content_types_queryset(self):
        """Return ContentType queryset based on models in url_support_content_types_models list."""
        support_models = []
        for content_item in self.url_support_content_types_models:
            support_models.append(content_item.content_model)
        content_types = ContentType.objects.get_for_models(*support_models)
        content_type_ids = [content_type.id for content_type in content_types.values()]
        return ContentType.objects.filter(id__in=content_type_ids)

    @cached_property
    def supported_content(self):
        return {content_type.content_model: content_type for content_type in self.url_support_content_types_models}

    def is_content_model_enabled(self, content_model):
        """Checks if provided content model is active for url manager."""
        return content_model in self.supported_content

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_models_support setting has been correctly set
        and add it to the masterlist if all is ok
        """
        # First check that url_manager_models_support is correctly defined
        if not hasattr(cms_config, 'url_manager_models_support'):
            raise ImproperlyConfigured(
                "url_manager_models_support must be defined in cms_config.py")
        if not isinstance(cms_config.url_manager_models_support, collections.abc.Iterable):
            raise ImproperlyConfigured(
                "url_manager_models_support not defined as an iterable")
        for models in cms_config.url_manager_models_support:
            if not isinstance(models, UrlContentItem):
                raise ImproperlyConfigured(
                    "{!r} is not a subclass of djangocms_url_manager.datastructures.UrlContentItem".format(models))
        self.url_support_content_types_models.extend(cms_config.url_manager_models_support)

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
