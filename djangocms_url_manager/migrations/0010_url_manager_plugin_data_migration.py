from django.db import migrations


def forwards(apps, schema_editor):
    LinkPlugin = apps.get_model('djangocms_url_manager', 'LinkPlugin')

    for link_plugin in LinkPlugin.objects.all():
        url = link_plugin.url
        link_plugin.url_grouper = url.url_grouper
        link_plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_url_manager', '0009_url_manager_data_migration'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
