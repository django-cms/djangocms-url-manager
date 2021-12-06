from functools import partial

from aldryn_client import forms


class Form(forms.BaseForm):
    def to_settings(self, data, settings):
        from aldryn_addons.utils import djsenv

        env = partial(djsenv, settings=settings)

        # Get a migration user if the env setting has been added
        migration_user_id = env(
            'DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID',
            default=False
        )
        if migration_user_id:
            settings['DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID'] = int(migration_user_id)

        settings["DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED"] = True
        return settings
