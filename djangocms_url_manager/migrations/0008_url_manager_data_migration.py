from django.apps import apps as global_apps
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations

from djangocms_url_manager.cms_config import UrlCMSAppConfig
from djangocms_url_manager.conf import (
    DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID,
)

try:
    from djangocms_versioning.constants import PUBLISHED

    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False


def forwards(apps, schema_editor):
    djangocms_versioning_config_enabled = UrlCMSAppConfig.djangocms_versioning_enabled
    ContentType = apps.get_model("contenttypes", "ContentType")
    Url = apps.get_model("djangocms_url_manager", "Url")
    UrlGrouper = apps.get_model("djangocms_url_manager", "UrlGrouper")
    User = apps.get_model('auth', 'User')

    # The test suite fails to find the Content type, in this scenario we
    # try and find the content type and create it if it doesn't yet exist using
    # ContentType.objects.get_for_model
    # This is the safest way because the following has been heavily manually tested already:
    # ContentType.objects.get(app_label='djangocms_url_manager', model='url')
    try:
        url_contenttype = ContentType.objects.get(app_label='djangocms_url_manager', model='url')
    except ContentType.DoesNotExist:
        url_contenttype = ContentType.objects.get_for_model(Url)

    url_queryset = Url.objects.all()

    if djangocms_versioning_config_enabled and djangocms_versioning_installed:
        # Get a migration user.
        migration_user = User.objects.get(id=DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID)
        Version = apps.get_model('djangocms_versioning', 'Version')

    for url in url_queryset:
        grouper = UrlGrouper.objects.create()
        grouper.internal_name = url.internal_name
        url.url_grouper = grouper
        url.save()

        # Create initial Url Versions if versioning is enabled and installed.
        if djangocms_versioning_config_enabled and djangocms_versioning_installed:
            # Keep the url date modified state in a version
            Version.objects.create(
                created_by=migration_user,
                state=PUBLISHED,
                number=1,
                object_id=url.pk,
                content_type=url_contenttype,
                modified=url.date_modified,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_url_manager", "0007_auto_20211124_0408")
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
