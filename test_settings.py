import os

from djangocms_url_manager.test_utils.polls.utils import (
    get_all_poll_content_objects,
    get_published_pages_objects,
)


EXTRA_INSTALLED_APPS = []
ENABLE_VERSIONING = bool(os.environ.get("ENABLE_VERSIONING", True))
if ENABLE_VERSIONING:
    EXTRA_INSTALLED_APPS.append("djangocms_versioning")

ENABLE_NAVIGATION = bool(os.environ.get("ENABLE_NAVIGATION", False))
if ENABLE_NAVIGATION:
    EXTRA_INSTALLED_APPS.append("djangocms_navigation")

ENABLE_MODERATION = bool(os.environ.get("ENABLE_MODERATION", True))
if ENABLE_MODERATION:
    EXTRA_INSTALLED_APPS.append("djangocms_moderation")

HELPER_SETTINGS = {
    "VERSIONING_CMS_MODELS_ENABLED": ENABLE_VERSIONING,
    "VERSIONING_URL_MANAGER_MODELS_ENABLED": ENABLE_VERSIONING,
    "MODERATING_URL_MANAGER_MODELS_ENABLED": ENABLE_MODERATION,
    "TOP_INSTALLED_APPS": ["djangocms_url_manager"],
    "INSTALLED_APPS": [
        "djangocms_url_manager.test_utils.polls",
        "djangocms_url_manager.test_utils.text",
    ]
    + EXTRA_INSTALLED_APPS,
    "MIGRATION_MODULES": {
        "sites": None,
        "contenttypes": None,
        "auth": None,
        "cms": None,
        "menus": None,
        "polls": None,
        "text": None,
        "djangocms_url_manager": None,
        "djangocms_versioning": None,
        "djangocms_navigation": None,
        "djangocms_moderation": None,
    },
    "CMS_PERMISSION": True,
    # At present, testing requires bootstrap to be disabled.
    # 'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    "LANGUAGES": (
        ("en", "English"),
        ("de", "German"),
        ("fr", "French"),
        ("it", "Italiano"),
    ),
    "CMS_LANGUAGES": {
        1: [
            {"code": "en", "name": "English", "fallbacks": ["de", "fr"]},
            {
                "code": "de",
                "name": "Deutsche",
                "fallbacks": ["en"],  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                "code": "fr",
                "name": "Française",
                "fallbacks": ["en"],  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                "code": "it",
                "name": "Italiano",
                "fallbacks": ["fr"],  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ]
    },
    "LANGUAGE_CODE": "en",
    "URL_MANAGER_SUPPORTED_MODELS": [
        ("cms.Page", get_published_pages_objects),
        ("polls.PollContent", get_all_poll_content_objects),
    ],
}


def run():
    from djangocms_helper import runner

    runner.cms("djangocms_url_manager", extra_args=[])


if __name__ == "__main__":
    run()
