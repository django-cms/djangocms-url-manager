from distutils.version import LooseVersion

import cms


CMS_VERSION = cms.__version__

CMS_36 = LooseVersion(CMS_VERSION) < LooseVersion("3.7")


def get_page_placeholders(page, language=None):
    try:
        # cms3.6 compat
        return page.get_placeholders()
    except TypeError:
        return page.get_placeholders(language)
