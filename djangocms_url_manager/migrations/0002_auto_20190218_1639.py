# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-18 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("djangocms_url_manager", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="linkplugin",
            name="internal_name",
            field=models.CharField(
                default=None, max_length=120, verbose_name="internal name"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="url",
            name="internal_name",
            field=models.CharField(
                blank=True,
                help_text="Provide internal name for URL objects for searching purpose",
                max_length=255,
                null=True,
                verbose_name="internal name",
            ),
        ),
        migrations.AddField(
            model_name="urloverride",
            name="internal_name",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="internal name",
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="content_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="contenttypes.ContentType",
            ),
        ),
        migrations.AlterField(
            model_name="urloverride",
            name="content_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="contenttypes.ContentType",
            ),
        ),
    ]
