from django.contrib import admin

from djangocms_url_manager.cms_config import UrlCMSAppConfig
from djangocms_url_manager.forms import UrlForm, UrlOverrideForm
from djangocms_url_manager.models import Url, UrlOverride
from djangocms_url_manager.urls import urlpatterns
from djangocms_url_manager.utils import is_versioning_enabled


# Use the version mixin if djangocms-versioning is installed and enabled
url_admin_classes = [admin.ModelAdmin]
url_admin_list_display = ("internal_name", "get_model_url", "date_modified",)
djangocms_versioning_enabled = UrlCMSAppConfig.djangocms_versioning_enabled

try:
    from djangocms_versioning.admin import ExtendedVersionAdminMixin

    if djangocms_versioning_enabled:
        url_admin_classes.insert(0, ExtendedVersionAdminMixin)
        url_admin_list_display = ("internal_name", "get_model_url",)
except ImportError:
    pass


__all__ = ["UrlAdmin", "UrlOverrideInlineAdmin"]


class UrlOverrideInlineAdmin(admin.StackedInline):
    model = UrlOverride
    form = UrlOverrideForm
    extra = 0


@admin.register(Url)
class UrlAdmin(*url_admin_classes):
    form = UrlForm
    inlines = [UrlOverrideInlineAdmin]
    list_display = url_admin_list_display
    search_fields = ("manual_url", "internal_name", "relative_path", "mailto", "phone")
    list_filter = ("site__name",)
    ordering = ("internal_name", "date_modified", )
    change_form_template = "admin/djangocms_url_manager/url/change_form.html"

    def get_urls(self):
        return urlpatterns + super().get_urls()

    def get_model_url(self, obj):
        return obj.get_url(obj.site)

    def get_search_results(self, request, queryset, search_term):
        """
        Override the ModelAdmin method for fetching search results to filter across the enabled content types
        :param request: Url Admin request
        :param queryset: Url queryset
        :param search_term: Term to be searched for
        :return: results
        """
        cms_config = UrlCMSAppConfig
        queryset, use_distinct = super(UrlAdmin, self).get_search_results(request, queryset, search_term)
        for model, search_helper in cms_config.url_manager_supported_models_search_helpers.items():
            queryset |= search_helper(model, queryset, search_term)

        return queryset, use_distinct

    get_model_url.short_description = "URL"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Provide additional context to the changeform
        extra_context['is_versioning_enabled'] = is_versioning_enabled()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
