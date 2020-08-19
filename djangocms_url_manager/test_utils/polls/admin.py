from django.contrib import admin

from djangocms_url_manager.test_utils.polls.models import PollContent


@admin.register(PollContent)
class PollAdmin(admin.ModelAdmin):
    list_display = ("poll", "language")

    class Meta:
        model = PollContent
