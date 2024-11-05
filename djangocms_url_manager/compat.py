import django

from packaging.version import Version

from cms import __version__ as CMS_VERSION


DJANGO_4_1 = Version(django.get_version()) < Version('4.2')
CMS_41 = Version("4.1") <= Version(CMS_VERSION)


def get_page_placeholders(page, language=None):
    try:
        # cms3.6 compat
        return page.get_placeholders()
    except TypeError:
        return page.get_placeholders(language)
