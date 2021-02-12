from distutils.version import LooseVersion

import cms


CMS_VERSION = cms.__version__

CMS_LT_4 = LooseVersion(CMS_VERSION) < LooseVersion("4.0")


def get_page_placeholders(page, language=None):
    try:
        # cms3.6 compat
        return page.get_placeholders()
    except TypeError:
        return page.get_placeholders(language)
