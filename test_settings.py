HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'INSTALLED_APPS': [
        'djangocms_url_manager',
    ],
    'CMS_PERMISSION': True,
    # At present, testing requires bootstrap to be disabled.
    # 'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
        ('it', 'Italiano'),
    ),
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', 'fr']
            },
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en']  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                'code': 'fr',
                'name': 'Française',
                'fallbacks': ['en']  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'fallbacks': ['fr']  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ],
    },
    'PARLER_LANGUAGES': {
        1: [
            {
                'code': 'en',
                'fallbacks': ['de', 'fr'],
                'hide_untranslated': False,
            },
            {
                'code': 'de',
                'fallbacks': ['en'],
                'hide_untranslated': False,
            },
            {
                'code': 'fr',
                'fallbacks': ['en'],
                'hide_untranslated': False,
            },
            {
                'code': 'it',
                'fallbacks': ['fr'],  # FOR TESTING, LEAVE AS ONLY 'fr'
                'hide_untranslated': False,
            },
        ],
        'default': {
            'code': 'en',
            'fallbacks': ['en'],
            'hide_untranslated': False,
        }
    },
    'PARLER_ENABLE_CACHING': False,
    'LANGUAGE_CODE': 'en',
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_url_manager', extra_args=[])


if __name__ == "__main__":
    run()
