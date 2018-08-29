from django.core.exceptions import ImproperlyConfigured


class UrlContentItem:

    def __init__(self, content_model):
        # We require get_absolute_url to be implemented on content models
        # because it is needed for django-cms's preview endpoint, which
        # is required by url manager.
        if not hasattr(content_model, 'get_absolute_url'):
            error_msg = "{} needs to implement get_absolute_url".format(
                    content_model.__name__)
            raise ImproperlyConfigured(error_msg)

        self.content_model = content_model
