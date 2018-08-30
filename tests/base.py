from django.contrib.sites.models import Site

from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse

from djangocms_url_manager.compat import get_page_placeholders
from djangocms_url_manager.constants import SELECT2_PAGE_URL_NAME
from djangocms_url_manager.models import Url as UrlModel, UrlOverride


class BaseUrlTestCase(CMSTestCase):
    select2_endpoint = admin_reverse(SELECT2_PAGE_URL_NAME)

    def setUp(self):
        self.language = 'en'
        self.page = create_page(
            title='test',
            template='page.html',
            language=self.language,
            in_navigation=True,
        )
        self.placeholder = get_page_placeholders(
            self.page,
            self.language,
        ).get(slot='content')
        self.superuser = self.get_superuser()
        self.default_site = Site.objects.first()
        self.site2 = Site.objects.create(
            name='foo.com',
            domain='foo.com',
        )
        self.page2 = create_page(
            title='test2',
            template='page.html',
            language=self.language,
            in_navigation=True,
            site=self.site2,
        )
        self.url = self._create_url(
            content_object=self.page,
        )
        self.urloverride = self._create_url_override(
            self.url,
            self.site2,
            self.page2,
        )

    def _create_url(self, site=None, content_object=None, manual_url='',
                    phone='', mailto='', anchor=''):
        if site is None:
            site = self.default_site

        return UrlModel.objects.create(
            site=site,
            content_object=content_object,
            manual_url=manual_url,
            phone=phone,
            mailto=mailto,
            anchor=anchor,
        )

    def _create_url_override(self, url, site, content_object=None, manual_url='',
                             phone='', mailto='', anchor=''):
        return UrlOverride.objects.create(
            url=url,
            site=site,
            content_object=content_object,
            manual_url=manual_url,
            phone=phone,
            mailto=mailto,
            anchor=anchor,
        )
