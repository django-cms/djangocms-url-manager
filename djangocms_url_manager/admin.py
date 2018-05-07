from django.contrib import admin

from .forms import UrlForm, UrlOverrideForm
from .models import Url, UrlOverride
from .urls import urlpatterns


__all__ = [
    'UrlAdmin',
    'UrlOverrideInlineAdmin',
]


class UrlOverrideInlineAdmin(admin.StackedInline):
    model = UrlOverride
    form = UrlOverrideForm
    extra = 0


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    form = UrlForm
    inlines = [UrlOverrideInlineAdmin]

    def get_urls(self):
        return urlpatterns + super().get_urls()
