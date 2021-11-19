from django.apps import apps as global_apps
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations

from djangocms_url_manager.cms_config import UrlCMSAppConfig
from djangocms_url_manager.conf import (
    DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID,
)

try:
    from djangocms_versioning.constants import DRAFT

    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False


def forwards(apps, schema_editor):
    create_contenttypes(global_apps.get_app_config("djangocms_url_manager"))

    djangocms_versioning_config_enabled = UrlCMSAppConfig.djangocms_versioning_enabled
    ContentType = apps.get_model("contenttypes", "ContentType")
    Url = apps.get_model("djangocms_url_manager", "Url")
    UrlGrouper = apps.get_model("djangocms_url_manager", "UrlGrouper")
    User = apps.get_model('auth', 'User')

    url_contenttype = ContentType.objects.get(app_label='djangocms_url_manager', model='url')
    url_queryset = Url.objects.all()

    for url in url_queryset:
        grouper = UrlGrouper.objects.create()
        grouper.internal_name = url.internal_name
        url.url_grouper = grouper
        url.save()

        # Get a migration user.
        migration_user = User.objects.get(id=DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID)

        # Create initial Url Versions if versioning is enabled and installed.
        if djangocms_versioning_config_enabled and djangocms_versioning_installed:
            Version = apps.get_model('djangocms_versioning', 'Version')
            Version.objects.create(
                created_by=migration_user,
                state=DRAFT,
                number=1,
                object_id=url.pk,
                content_type=url_contenttype,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_url_manager", "0007_auto_20211112_1245")
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
