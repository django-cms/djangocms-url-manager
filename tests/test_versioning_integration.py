from django.contrib.sites.models import Site

from cms.api import add_plugin, create_page
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url

from djangocms_versioning.models import Version

from djangocms_url_manager.models import (
    UrlGrouper,
    Url as UrlModel,
    UrlOverride,
)


class VersioningIntegrationTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.user = self.get_superuser()
        self.site = Site.objects.first()
        self.url_grouper = UrlGrouper.objects.create()
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.user,
        )
        pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        pagecontent_version = pagecontent.versions.first()
        pagecontent_version.publish(self.user)

    def test_version_copy_method(self):
        """
        Creating a draft version from a published version copies the form correctly
        """
        url_content = UrlModel.objects.create(
            internal_name="some url",
            site=self.site,
            content_object=self.page,
            manual_url="http://www.fake-test.com",
            relative_path="some/extra/long/path/",
            anchor="some-page-anchor",
            mailto="mike.smith@fake-test.com",
            phone="00000000000",
            url_grouper=self.url_grouper,
        )
        original_version = Version.objects.create(
            content=url_content,
            created_by=self.user,
        )
        new_version = original_version.copy(self.user)

        # Created a new content record
        self.assertNotEqual(original_version.content.pk, new_version.content.pk)
        # Is version of the same grouper as the original version
        self.assertEqual(original_version.content.url_grouper, new_version.content.url_grouper)
        # The content items have bene duplicated correctly
        original_content = original_version.content
        new_content = new_version.content
        self.assertEqual(original_content.internal_name, new_content.internal_name)
        self.assertEqual(original_content.site, new_content.site)
        # Url types
        self.assertEqual(original_content.content_object, new_content.content_object)
        self.assertEqual(original_content.manual_url, new_content.manual_url)
        self.assertEqual(original_content.relative_path, new_content.relative_path)
        self.assertEqual(original_content.anchor, new_content.anchor)
        self.assertEqual(original_content.mailto, new_content.mailto)
        self.assertEqual(original_content.phone, new_content.phone)

    # TODO: Overrides!!!
    def test_version_copy_method_attached_overrides(self):
        url_content = UrlModel.objects.create(
            internal_name="some url",
            site=self.site,
            relative_path="some/extra/long/path/",
            url_grouper=self.url_grouper,
        )
        url_content_override = UrlOverride.objects.create(
            url=url_content,
            site=self.site,
            content_object=self.page,
            manual_url="http://www.fake-another-test.com",
            relative_path="some/other/extra/long/path/",
            anchor="some-other-page-anchor",
            mailto="mike.smith@another-fake-test.com",
            phone="00000000000",
        )
        original_version = Version.objects.create(
            content=url_content,
            created_by=self.user,
        )
        new_version = original_version.copy(self.user)

        original_content_override = url_content_override
        new_content_override = UrlOverride.objects.get(url=new_version.content.pk)

        # The content attached items have been duplicated correctly
        self.assertNotEqual(original_content_override.pk, new_content_override.pk)
        self.assertEqual(original_content_override.internal_name, new_content_override.internal_name)
        self.assertEqual(original_content_override.site, new_content_override.site)
        # Url override types
        self.assertEqual(original_content_override.content_object, new_content_override.content_object)
        self.assertEqual(original_content_override.manual_url, new_content_override.manual_url)
        self.assertEqual(original_content_override.relative_path, new_content_override.relative_path)
        self.assertEqual(original_content_override.anchor, new_content_override.anchor)
        self.assertEqual(original_content_override.mailto, new_content_override.mailto)
        self.assertEqual(original_content_override.phone, new_content_override.phone)


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
