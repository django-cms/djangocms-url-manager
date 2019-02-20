from django.contrib.sites.models import Site

from djangocms_url_manager.forms import ContentTypeObjectSelectWidget, UrlForm, UrlOverrideForm

from .base import BaseUrlTestCase


class UrlManagerFormsTestCase(BaseUrlTestCase):
    def test_url_override_form(self):
        site3 = Site.objects.create(name="bar.com", domain="bar.com")
        form = UrlOverrideForm(
            {"url": self.url.pk, "site": site3.pk, "url_type": "manual_url", "manual_url": "http://google.com/"}
        )
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.site_id, site3.pk),
        self.assertEqual(instance.manual_url, "http://google.com/"),
        self.assertEqual(instance.content_type_id, None),
        self.assertEqual(instance.object_id, None),
        self.assertEqual(instance.anchor, ""),
        self.assertEqual(instance.mailto, ""),
        self.assertEqual(instance.phone, ""),
        self.assertEqual(instance.url_id, self.url.pk),

    def test_url_override_form_disallow_same_site_as_original_url(self):
        form = UrlOverrideForm({"url": self.url.pk, "site": self.url.site_id})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "url_type": ["This field is required."],
                "content_object": ["Field is required"],
                "site": ["Overriden site must be different from the original."],
            },
        )

    def test_data_select_widget_build_attrs(self):
        self.assertDictContainsSubset(
            ContentTypeObjectSelectWidget().build_attrs({}), {"data-select2-url": self.select2_endpoint}
        )

    def test_url_form_empty_data(self):
        form = UrlForm({"site": self.default_site})
        self.assertFalse(form.is_valid())

    def test_url_form_url_type_choices(self):
        form = UrlForm()
        self.assertListEqual(
            form.fields["url_type"].choices,
            [
                (self.page_contenttype_id, "Page"),
                (self.poll_content_contenttype_id, "Poll content"),
                ("manual_url", "Manual URL"),
                ("anchor", "Anchor"),
                ("mailto", "Email address"),
                ("phone", "Phone"),
            ],
        )

    def test_url_form_create_url_with_valid_manual_url(self):
        form = UrlForm(
            {
                "site": self.default_site.id,
                "url_type": "manual_url",
                "manual_url": "https://google.com/",
                "anchor": "test",
                "mailto": "test@gmail.com",
                "phone": "112",
                "content_object": self.page.id,
            }
        )
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.site_id, self.default_site.id)
        self.assertEqual(instance.manual_url, "https://google.com/")
        self.assertEqual(instance.anchor, "")
        self.assertEqual(instance.mailto, "")
        self.assertEqual(instance.phone, "")
        self.assertEqual(instance.content_type_id, None)
        self.assertEqual(instance.object_id, None)

    def test_url_form_create_url_with_invalid_manual_url(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "manual_url", "manual_url": "google"})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"manual_url": ["Enter a valid URL."]})

    def test_url_form_create_url_with_empty_manual_url(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "manual_url", "manual_url": ""})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"manual_url": ["Field is required"]})

    def test_url_form_create_url_with_valid_anchor(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "anchor", "anchor": "test"})
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.anchor, "test")

    def test_url_form_create_url_with_invalid_anchor(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "anchor", "anchor": "#example"})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"anchor": ['Do not include a preceding "#" symbol.']})

    def test_url_form_create_url_with_empty_anchor(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "anchor", "anchor": ""})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"anchor": ["Field is required"]})

    def test_url_form_create_url_with_valid_mailto(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "mailto", "mailto": "norman.burdett@gmail.com"})
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.mailto, "norman.burdett@gmail.com")

    def test_url_form_create_url_with_invalid_mailto(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "mailto", "mailto": "norman"})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"mailto": ["Enter a valid email address."]})

    def test_url_form_create_url_with_empty_mailto(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "mailto", "mailto": ""})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"mailto": ["Field is required"]})

    def test_url_form_create_url_with_valid_phone(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "phone", "phone": "+44 20 7946 0916"})
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.phone, "+44 20 7946 0916")

    def test_url_form_create_url_with_empty_phone(self):
        form = UrlForm({"site": self.default_site.id, "url_type": "phone", "phone": ""})
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"phone": ["Field is required"]})

    def test_url_form_create_url_with_valid_page_content_and_content_object(self):
        form = UrlForm(
            {
                "site": self.site2.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page2.pk,
                "manual_url": "http://google.com/",
                "anchor": "test",
                "mailto": "test@gmail.com",
                "phone": "112",
            }
        )
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.site_id, self.site2.id)
        self.assertEqual(instance.content_type_id, self.page_contenttype_id)
        self.assertEqual(instance.object_id, self.page2.id)
        self.assertEqual(instance.manual_url, "")
        self.assertEqual(instance.anchor, "")
        self.assertEqual(instance.mailto, "")
        self.assertEqual(instance.phone, "")

    def test_create_url_for_content_object_that_already_have_url(self):
        form = UrlForm(
            {
                "site": self.default_site.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page.pk,
                "manual_url": "http://google.com/",
                "anchor": "test",
                "mailto": "test@gmail.com",
                "phone": "112",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"content_object": ["Url with this object already exists"]})

    def test_url_form_create_url_with_invalid_content_type_and_content_object(self):
        form = UrlForm({"site": self.default_site.id, "url_type": 99, "content_object": 99})
        self.assertDictEqual(
            form.errors,
            {
                "url_type": ["Select a valid choice. 99 is not one of the available choices."],
                "content_object": [
                    "Object does not exist in a given content type id: {} and site: {}".format(99, self.default_site)
                ],
            },
        )

    def test_url_form_create_url_with_empty_content_object(self):
        form = UrlForm({"site": self.default_site.id, "url_type": self.page_contenttype_id, "content_object": None})
        self.assertDictEqual(form.errors, {"content_object": ["Field is required"]})

    def test_url_override_form_dont_validate_object_already_exists(self):
        self._create_url(site=self.site2, content_object=self.page2)
        form = UrlOverrideForm(
            {
                # self.url is with self.default_site and self.page
                "url": self.url.pk,
                "site": self.site2.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page2.pk,
            }
        )
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.site_id, self.site2.pk),
        self.assertEqual(instance.content_type_id, self.page_contenttype_id),
        self.assertEqual(instance.object_id, self.page2.pk),
        self.assertEqual(instance.anchor, ""),
        self.assertEqual(instance.manual_url, ""),
        self.assertEqual(instance.mailto, ""),
        self.assertEqual(instance.phone, ""),
        self.assertEqual(instance.url_id, self.url.pk),

    def test_url_override_form_validate_object_with_this_site_and_object_already_exists(self):
        self._create_url_override(self.url, self.site2, self.page2)
        form = UrlOverrideForm(
            {
                # self.url is with self.default_site and self.page
                "url": self.url.pk,
                "site": self.site2.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page2.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"__all__": ["Url override with this Site and Url already exists."]})
