from django.contrib.sites.models import Site

from cms.api import add_plugin, create_page
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url

from djangocms_versioning.models import Version

from djangocms_url_manager.models import UrlOverride
from djangocms_url_manager.test_utils.factories import (
    UrlFactory,
    UrlGrouperFactory,
    UrlOverrideFactory,
)


class VersioningIntegrationTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.user = self.get_superuser()
        self.site = Site.objects.first()
        self.url_grouper = UrlGrouperFactory()
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
        url_content = UrlFactory(
            url_grouper=self.url_grouper,
            site=self.site,
            content_object=self.page,
            manual_url="http://www.fake-test.com",
            relative_path="some/extra/long/path/",
            anchor="some-page-anchor",
            mailto="mike.smith@fake-test.com",
            phone="00000000000",
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

    def test_version_copy_method_attached_overrides(self):
        site2 = Site.objects.create(name="another-site.com", domain="another-site.com")
        url_content = UrlFactory(
            url_grouper=self.url_grouper,
            site=self.site,
            relative_path="some/extra/long/path/",
        )
        url_content_override_1 = UrlOverrideFactory(
            url=url_content,
            site=self.site,
            content_object=self.page,
            manual_url="http://www.override1.com",
            relative_path="override1/path/",
            anchor="override1-anchor",
            mailto="mike.smith@override1.com",
            phone="11111111111",
        )
        url_content_override_2 = UrlOverrideFactory(
            url=url_content,
            site=site2,
            content_object=self.page,
            manual_url="http://www.override2.com",
            relative_path="override2/path/",
            anchor="override2-anchor",
            mailto="mike.smith@override2.com",
            phone="22222222222",
        )
        original_version = Version.objects.create(
            content=url_content,
            created_by=self.user,
        )
        new_version = original_version.copy(self.user)

        # The content attached items have been duplicated correctly
        # Url override 1
        new_content_override_1 = UrlOverride.objects.get(
            url=new_version.content.pk,
            mailto="mike.smith@override1.com",
        )

        self.assertNotEqual(url_content_override_1.pk, new_content_override_1.pk)
        self.assertEqual(url_content_override_1.internal_name, new_content_override_1.internal_name)
        self.assertEqual(url_content_override_1.site, new_content_override_1.site)
        # Url override types
        self.assertEqual(url_content_override_1.content_object, new_content_override_1.content_object)
        self.assertEqual(url_content_override_1.manual_url, new_content_override_1.manual_url)
        self.assertEqual(url_content_override_1.relative_path, new_content_override_1.relative_path)
        self.assertEqual(url_content_override_1.anchor, new_content_override_1.anchor)
        self.assertEqual(url_content_override_1.mailto, new_content_override_1.mailto)
        self.assertEqual(url_content_override_1.phone, new_content_override_1.phone)

        # Url override 2
        new_content_override_2 = UrlOverride.objects.get(
            url=new_version.content.pk,
            mailto="mike.smith@override2.com",
        )

        self.assertNotEqual(url_content_override_2.pk, new_content_override_2.pk)
        self.assertEqual(url_content_override_2.internal_name, new_content_override_2.internal_name)
        self.assertEqual(url_content_override_2.site, new_content_override_2.site)
        # Url override types
        self.assertEqual(url_content_override_2.content_object, new_content_override_2.content_object)
        self.assertEqual(url_content_override_2.manual_url, new_content_override_2.manual_url)
        self.assertEqual(url_content_override_2.relative_path, new_content_override_2.relative_path)
        self.assertEqual(url_content_override_2.anchor, new_content_override_2.anchor)
        self.assertEqual(url_content_override_2.mailto, new_content_override_2.mailto)
        self.assertEqual(url_content_override_2.phone, new_content_override_2.phone)


class VersioningCMSPageIntegrationTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.user = self.get_superuser()
        self.site = Site.objects.first()

        self.url_grouper = UrlGrouperFactory()
        self.url_content = UrlFactory(
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
