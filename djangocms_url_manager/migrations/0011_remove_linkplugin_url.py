# Generated by Django 2.2.24 on 2021-11-23 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_url_manager', '0010_url_manager_plugin_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkplugin',
            name='url',
        ),
    ]
