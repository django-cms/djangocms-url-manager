from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.models import Page
from cms.utils.urlutils import admin_reverse

from djangocms_url_manager.compat import CMS_36

from .constants import SELECT2_PAGE_URL_NAME
from .models import Url, UrlOverride


class Select2Mixin:

    class Media:
        css = {
            'all': ('cms/js/select2/select2.css', ),
        }
        js = (
            'cms/js/select2/select2.js',
            'djangocms_url_manager/js/create_url.js',
        )


class SiteSelectWidget(Select2Mixin, forms.Select):
    pass


class PageSelectWidget(Select2Mixin, forms.TextInput):

    def get_url(self):
        return admin_reverse(SELECT2_PAGE_URL_NAME)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('data-select2-url', self.get_url())
        return attrs


class UrlForm(forms.ModelForm):
    site = forms.ModelChoiceField(
        label=_('Site'),
        queryset=Page.objects.drafts() if CMS_36 else Site.objects.all(),
        widget=SiteSelectWidget(
            attrs={
                'data-placeholder': _('Select site to choose pages from'),
            },
        ),
        empty_label='',
    )
    page = forms.ModelChoiceField(
        label=_('Page'),
        queryset=Page.objects.drafts() if CMS_36 else Site.objects.all(),
        widget=PageSelectWidget(
            attrs={
                'data-placeholder': _('Select a page'),
            },
        ),
        required=False,
    )

    class Meta:
        model = Url
        fields = (
            'site', 'manual_url', 'page', 'anchor', 'mailto', 'phone',
        )


class UrlOverrideForm(forms.ModelForm):
    site = forms.ModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all(),
        widget=SiteSelectWidget(
            attrs={
                'data-placeholder': _('Select site to choose pages from'),
            },
        ),
        empty_label='',
    )
    page = forms.ModelChoiceField(
        label=_('Page'),
        queryset=Page.objects.all(),
        widget=PageSelectWidget(
            attrs={
                'data-placeholder': _('Select a page'),
            },
        ),
        required=False,
    )

    class Meta:
        model = UrlOverride
        fields = (
            'url', 'site', 'manual_url', 'page', 'anchor', 'mailto', 'phone',
        )

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        site = cleaned_data.get('site')

        if url and url.site == site:
            raise forms.ValidationError({
                'site': _('Overriden site must be different from the original.'),  # noqa: E501
            })

        return cleaned_data
