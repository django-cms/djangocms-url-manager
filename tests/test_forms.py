from django.contrib.sites.models import Site

from djangocms_url_manager.forms import PageSelectWidget, UrlOverrideForm

from .base import BaseUrlManagerPluginTestCase


class UrlManagerFormsTestCase(BaseUrlManagerPluginTestCase):

    def test_urloverrideform(self):
        site3 = Site.objects.create(
            name='bar.com',
            domain='bar.com',
        )
        form = UrlOverrideForm({
            'url': self.url.pk,
            'site': site3.pk,
        })
        self.assertTrue(form.is_valid())

    def test_urloverrideform_disallow_same_site_as_original_url(self):
        form = UrlOverrideForm({
            'url': self.url.pk,
            'site': self.url.site_id,
        })
        self.assertFalse(form.is_valid())

    def test_page_select_widget_build_attrs(self):
        self.assertDictContainsSubset(
            PageSelectWidget().build_attrs({}),
            {'data-select2-url': self.select2_endpoint},
        )
