from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from cms.models import Page, PageContent

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
    search_fields = ("manual_url", "internal_name", "relative_path", "mailto", "phone")
    list_filter = ("site__name",)
    ordering = ("internal_name", "date_modified", )

    def get_urls(self):
        return urlpatterns + super().get_urls()

    def get_model_url(self, obj):
        return obj.get_url(obj.site)

    def get_search_results(self, request, queryset, search_term):
        """
        Override the ModelAdmin method for fetching search results to filter across a the enabled content type (Page)
        :param request: Url Admin request
        :param queryset: Url queryset
        :param search_term: Term to be searched for
        :return: results
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        page_content_queryset = PageContent.objects.filter(title=search_term)
        content_type_id = ContentType.objects.get_for_model(Page).id

        for page_content in page_content_queryset:
            try:
                queryset |= self.model.objects.filter(
                    object_id=page_content.page.id,
                    content_type=content_type_id
                )
            except BaseException:
                pass

        return queryset, use_distinct

    get_model_url.short_description = "URL"
