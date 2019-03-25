from aldryn_client import forms


class Form(forms.BaseForm):
    def to_settings(self, data, settings):
        settings["DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED"] = True
        return settings
