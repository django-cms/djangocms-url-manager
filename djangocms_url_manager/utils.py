import collections

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase

from djangocms_url_manager.compat import CMS_36


def validate_settings(config, attr_name):
    """Validates settings for url manager"""
    if not hasattr(config, attr_name):
        raise ImproperlyConfigured(
            "{} must be defined in your {}".format(
                attr_name,
                'settings' if CMS_36 else 'cms_config',
            )
        )
    if not isinstance(getattr(config, attr_name), collections.Iterable):
        raise ImproperlyConfigured(
            "{} not defined as an ".format(attr_name))

    if CMS_36:
        models = supported_models()
    else:
        models = getattr(config, attr_name)

    for model in models:
        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured(
                "{!r} is not a subclass of django.db.models.base.ModelBase".format(model))
        if not hasattr(model, 'get_absolute_url'):
            raise ImproperlyConfigured(
                "{} needs to implement get_absolute_url method".format(model.__name__))


def supported_models():
    """Return a list with supported models to use with url manager"""
    if CMS_36:
        models = []
        for app_label in getattr(settings, 'URL_MANAGER_SUPPORTED_MODELS', []):
            try:
                models.append(apps.get_model(app_label))
            except ValueError:
                return '"{}" is not valid path to model'.format(app_label)
        return models
    else:
        extension = apps.get_app_config('djangocms_url_manager').cms_extension
        return extension.url_manager_supported_models


def is_model_supported(model):
    """Checks if model is supported to use with url manager"""
    return model in supported_models()
