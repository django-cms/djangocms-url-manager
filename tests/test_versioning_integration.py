from django.contrib.sites.models import Site

from cms.api import add_plugin, create_page
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url

from djangocms_versioning.models import Version

from djangocms_url_manager.models import UrlGrouper, Url as UrlModel


class VersioningIntegrationTestCase(CMSTestCase):
    def test_version_copy_method(self):
        """
        Creating a draft version from a published version copies the form correctly
        """
        self.assertTrue(False)


class VersioningCMSPageIntegrationTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.user = self.get_superuser()
        self.site = Site.objects.first()

        self.url_grouper = UrlGrouper.objects.create()
        self.url_content = UrlModel.objects.create(
            internal_name="url 1",
            site=self.site,
            relative_path="some/path/",
            url_grouper=self.url_grouper,
        )
        self.url_content_version = Version.objects.create(
            content=self.url_content,
            created_by=self.user,
        )

        # Create a page
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.user,
        )
        # Publish the page content
        self.published_pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        published_pagecontent_version = self.published_pagecontent.versions.first()
        published_pagecontent_version.publish(self.user)
        # Create a draft page_content
        draft_pagecontent_version = published_pagecontent_version.copy(self.user)
        self.draft_pagecontent = draft_pagecontent_version.content

    def test_edit_endpoint_published_page_rendering_published_url(self):
        self.url_content_version.publish(user=self.user)

        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Published URL plugin",
        )

        request_url = get_object_edit_url(self.published_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "some/path/")

    def test_edit_endpoint_draft_page_rendering_published_url(self):
        self.url_content_version.publish(user=self.get_superuser())

        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Published URL plugin",
        )

        request_url = get_object_edit_url(self.draft_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "some/path/")

    def test_edit_endpoint_published_page_rendering_draft_url(self):
        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Draft URL plugin",
        )

        request_url = get_object_edit_url(self.published_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "some/path/")

    def test_edit_endpoint_draft_page_rendering_draft_url(self):
        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Draft URL plugin",
        )

        request_url = get_object_edit_url(self.draft_pagecontent, self.language)
        with self.login_user_context(self.user):
            response = self.client.get(request_url)

        self.assertContains(response, "some/path/")

    def test_live_endpoint_published_page_draft_url(self):
        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Draft URL plugin",
        )

        request_url = self.page.get_absolute_url(self.language)
        response = self.client.get(request_url)

        self.assertNotContains(response, "some/path/")

    def test_live_endpoint_published_page_published_url(self):
        self.url_content_version.publish(user=self.get_superuser())

        add_plugin(
            self.published_pagecontent.placeholders.get(slot="content"),
            "HtmlLink",
            language=self.language,
            url_grouper=self.url_grouper,
            label="Published URL plugin",
        )

        request_url = self.page.get_absolute_url(self.language)
        response = self.client.get(request_url)

        self.assertContains(response, "some/path/")
