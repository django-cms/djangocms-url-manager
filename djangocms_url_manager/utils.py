import functools
from collections import OrderedDict
from collections.abc import Iterable
from functools import lru_cache

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase

from cms.models import PageContent

from djangocms_url_manager.compat import CMS_36


def parse_settings(config, attr_name):
    url_manager_supported_models = OrderedDict()
    if not hasattr(config, attr_name):
        raise ImproperlyConfigured(
            "{} must be defined in your {}".format(
                attr_name, "settings" if CMS_36 else "cms_config"
            )
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
            raise ImproperlyConfigured(
                '"{}" app for this model is not in INSTALLED_APPS'.format(model)
            )
        except ValueError:
            raise ImproperlyConfigured('"{}" is not valid path to model'.format(model))

        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured(
                "{!r} is not a subclass of django.db.models.base.ModelBase".format(
                    model
                )
            )
        if not hasattr(model, "get_absolute_url"):
            raise ImproperlyConfigured(
                "{} needs to implement get_absolute_url method".format(model.__name__)
            )
        if model in url_manager_supported_models.keys():
            raise ImproperlyConfigured(
                "Model {!r} is duplicated in url_manager_supported_models".format(
                    model.__name__
                )
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


@lru_cache(maxsize=1)
def supported_models_search_helpers():
    app_config = apps.get_app_config("djangocms_url_manager")
    try:
        extension = app_config.cms_extension
        return extension.url_manager_supported_models_search_helpers
    except AttributeError:
        return app_config.url_manager_supported_models_search_helpers


def is_model_supported(model):
    """Return bool value if model is in keys"""
    return model in supported_models().keys()


def is_versioning_enabled():
    from djangocms_url_manager.models import Url
    try:
        app_config = apps.get_app_config('djangocms_versioning')
        return app_config.cms_extension.is_content_model_versioned(Url)
    except LookupError:
        return False


def get_supported_model_queryset(model):
    func = supported_models()[model]
    if func:
        return functools.partial(func, model)


def get_page_search_results(model, queryset, search_term):
    """
    A helper method to filter across generic foreign key relations.
    Provide additional helpers for any models when extending this app.
    :param model: The supported model
    :param queryset: The queryset to be filtered
    :param search_term: Term to be searched for
    :return: results
    """
    from djangocms_url_manager.models import Url
    page_content_queryset = PageContent._base_manager.filter(title__icontains=search_term)
    content_type_id = ContentType.objects.get_for_model(model).id

    for page_content in page_content_queryset:
        try:
            queryset |= Url._base_manager.filter(
                object_id=page_content.page.id,
                content_type=content_type_id
            )
        except BaseException:
            pass

    return queryset
