import django

from packaging.version import Version


DJANGO_4_1 = Version(django.get_version()) < Version('4.2')


def get_page_placeholders(page, language=None):
    try:
        # cms3.6 compat
        return page.get_placeholders()
    except TypeError:
        return page.get_placeholders(language)
