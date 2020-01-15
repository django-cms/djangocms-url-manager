from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site

from .forms import UrlForm, UrlOverrideForm
from .models import Url, UrlOverride
from .urls import urlpatterns


__all__ = ["UrlAdmin", "UrlOverrideInlineAdmin"]


class UrlOverrideInlineAdmin(admin.StackedInline):
    model = UrlOverride
    form = UrlOverrideForm
    extra = 0


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    form = UrlForm
    inlines = [UrlOverrideInlineAdmin]
    list_display = ("internal_name", "get_model_url", "date_modified", )
    search_fields = ("manual_url", "internal_name",)
    list_filter = ("site__name", "content_type",)
    ordering = ("internal_name", "date_modified", )

    def get_urls(self):
        return urlpatterns + super().get_urls()

    def get_model_url(self, obj):
        return obj.get_url(obj.site)

    get_model_url.short_description = "URL"
