HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'INSTALLED_APPS': [
        'djangocms_url_manager',
        'djangocms_url_manager.test_utils.polls',
    ],
    'MIGRATION_MODULES': {
        'sites': None,
        'contenttypes': None,
        'auth': None,
        'cms': None,
        'menus': None,
        'polls': None,
        'djangocms_url_manager': None,
    },
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
    'LANGUAGE_CODE': 'en',
    'URL_MANAGER_SUPPORTED_MODELS': [
        'cms.Page',
        'polls.PollContent',
    ]
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_url_manager', extra_args=[])


if __name__ == "__main__":
    run()
