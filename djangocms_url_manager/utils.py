from collections import Iterable
from functools import lru_cache

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase

from djangocms_url_manager.compat import CMS_36


def validate_settings(config, attr_name):
    if not hasattr(config, attr_name):
        raise ImproperlyConfigured(
            "{} must be defined in your {}".format(
                attr_name,
                'settings' if CMS_36 else 'cms_config',
            )
        )
    models = getattr(config, attr_name)
    if not isinstance(models, Iterable):
        raise ImproperlyConfigured(
            "{} not defined as an Iterable".format(attr_name))

    for model in models:
        if isinstance(model, str):
            try:
                model = apps.get_model(model)
            except LookupError:
                raise ImproperlyConfigured('"{}" app for this model is not in INSTALLED_APPS'.format(model))
            except ValueError:
                raise ImproperlyConfigured('"{}" is not valid path to model'.format(model))
        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured(
                "{!r} is not a subclass of django.db.models.base.ModelBase".format(model))
        if not hasattr(model, 'get_absolute_url'):
            raise ImproperlyConfigured(
                "{} needs to implement get_absolute_url method".format(model.__name__))


@lru_cache(maxsize=1)
def supported_models():
    try:
        extension = apps.get_app_config('djangocms_url_manager').cms_extension
        return extension.url_manager_supported_models
    except AttributeError:
        url_manager_supported_models = []
        for model in getattr(settings, 'URL_MANAGER_SUPPORTED_MODELS', []):
            if model not in url_manager_supported_models:
                url_manager_supported_models.append(apps.get_model(model))
        return url_manager_supported_models


def is_model_supported(model):
    return model in supported_models()
