import functools
from collections import Iterable, OrderedDict
from functools import lru_cache

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase

from djangocms_url_manager.compat import CMS_36


def parse_settings(config, attr_name):
    url_manager_supported_models = OrderedDict()
    if not hasattr(config, attr_name):
        raise ImproperlyConfigured(
            "{} must be defined in your {}".format(attr_name, "settings" if CMS_36 else "cms_config")
        )
    models = getattr(config, attr_name)
    if not isinstance(models, Iterable):
        raise ImproperlyConfigured("{} not defined as an Iterable".format(attr_name))

    for model in models:
        # model can be just a model class, or a (model class, function returning queryset) tuple
        try:
            model, func = model
        except (TypeError, ValueError):
            func = None

        try:
            if isinstance(model, str):
                model = apps.get_model(model)
        except LookupError:
            raise ImproperlyConfigured('"{}" app for this model is not in INSTALLED_APPS'.format(model))
        except ValueError:
            raise ImproperlyConfigured('"{}" is not valid path to model'.format(model))

        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured("{!r} is not a subclass of django.db.models.base.ModelBase".format(model))
        if not hasattr(model, "get_absolute_url"):
            raise ImproperlyConfigured("{} needs to implement get_absolute_url method".format(model.__name__))
        if model in url_manager_supported_models.keys():
            raise ImproperlyConfigured(
                "Model {!r} is duplicated in url_manager_supported_models".format(model.__name__)
            )

        url_manager_supported_models[model] = func

    return url_manager_supported_models


@lru_cache(maxsize=1)
def supported_models():
    app_config = apps.get_app_config("djangocms_url_manager")
    try:
        extension = app_config.cms_extension
        return extension.url_manager_supported_models
    except AttributeError:
        return app_config.url_manager_supported_models


def is_model_supported(model):
    """Return bool value if model is in keys"""
    return model in supported_models().keys()


def get_supported_model_queryset(model):
    func = supported_models()[model]
    if func:
        return functools.partial(func, model)
