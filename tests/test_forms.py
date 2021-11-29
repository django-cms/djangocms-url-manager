from urllib.parse import urlparse

from djangocms_url_manager.forms import (
    ContentTypeObjectSelectWidget,
    UrlForm,
)

from .base import BaseUrlTestCase


class UrlManagerFormsTestCase(BaseUrlTestCase):

    def test_data_select_widget_build_attrs(self):
        self.assertDictContainsSubset(
            ContentTypeObjectSelectWidget().build_attrs({}),
            {"data-select2-url": self.select2_endpoint},
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
                ("relative_path", "Relative path"),
                ("anchor", "Anchor"),
                ("mailto", "Email address"),
                ("phone", "Phone"),
            ],
        )

    def test_url_form_create_url_with_valid_manual_url(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.id,
                "url_type": "manual_url",
                "manual_url": "https://google.com/",
                "relative_path": "/some/random/path",
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
        self.assertEqual(instance.relative_path, "")
        self.assertEqual(instance.anchor, "")
        self.assertEqual(instance.mailto, "")
        self.assertEqual(instance.phone, "")
        self.assertEqual(instance.content_type_id, None)
        self.assertEqual(instance.object_id, None)

    def test_url_form_create_url_with_invalid_manual_url(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.id,
                "url_type": "manual_url",
                "manual_url": "google",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"manual_url": ["Enter a valid URL."]})

    def test_url_form_create_url_with_empty_manual_url(self):
        form = UrlForm(
            {"internal_name": "Test Name", "site": self.default_site.id, "url_type": "manual_url", "manual_url": ""}
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"manual_url": ["Field is required"]})

    def test_url_form_create_url_with_valid_relative_path(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.id,
                "url_type": "relative_path",
                "manual_url": "https://google.com/",
                "relative_path": "/some/random/path",
                "anchor": "test",
                "mailto": "test@gmail.com",
                "phone": "112",
                "content_object": self.page.id,
            }
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.site_id, self.default_site.id)
        self.assertEqual(instance.manual_url, "")
        self.assertEqual(instance.relative_path, "/some/random/path")
        self.assertEqual(instance.anchor, "")
        self.assertEqual(instance.mailto, "")
        self.assertEqual(instance.phone, "")
        self.assertEqual(instance.content_type_id, None)
        self.assertEqual(instance.object_id, None)

    def test_url_form_create_url_with_empty_relative_path(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.id,
                "url_type": "relative_path",
                "relative_path": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"relative_path": ["Field is required"]})

    def test_url_form_create_url_with_valid_anchor(self):
        form = UrlForm(
            {"internal_name": "Test Name", "site": self.default_site.id, "url_type": "anchor", "anchor": "test"}
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.anchor, "test")

    def test_url_form_create_url_with_invalid_anchor(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.id,
                "url_type": "anchor", "anchor": "#example"
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors, {"anchor": ['Do not include a preceding "#" symbol.']}
        )

    def test_url_form_create_url_with_empty_anchor(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": "anchor",
                "anchor": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"anchor": ["Field is required"]})

    def test_url_form_create_url_with_valid_mailto(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": "mailto",
                "mailto": "norman.burdett@gmail.com",
            }
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.mailto, "norman.burdett@gmail.com")

    def test_url_form_create_url_with_invalid_mailto(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": "mailto",
                "mailto": "norman"
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"mailto": ["Enter a valid email address."]})

    def test_url_form_create_url_with_empty_mailto(self):
        form = UrlForm(
            {"internal_name": "Test Name", "site": self.default_site.id, "url_type": "mailto", "mailto": ""}
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"mailto": ["Field is required"]})

    def test_url_form_create_url_with_valid_phone(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": "phone",
                "phone": "+44 20 7946 0916",
            }
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.phone, "+44 20 7946 0916")

    def test_url_form_create_url_with_empty_phone(self):
        form = UrlForm({"internal_name": "Test Name", "site": self.default_site.id, "url_type": "phone", "phone": ""})

        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"phone": ["Field is required"]})

    def test_url_form_create_url_with_valid_page_content_and_content_object(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.site2.pk,
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

        self.assertEqual(instance.site_id, self.site2.pk)
        self.assertEqual(instance.content_type_id, self.page_contenttype_id)
        self.assertEqual(instance.object_id, self.page2.pk)
        self.assertEqual(instance.manual_url, "")
        self.assertEqual(instance.relative_path, "")
        self.assertEqual(instance.anchor, "")
        self.assertEqual(instance.mailto, "")
        self.assertEqual(instance.phone, "")

    def test_create_url_for_content_object_that_already_have_url(self):
        self.url.versions.first().publish(user=self.superuser)
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": self.page_contenttype_id,
                "content_object": self.page.pk,
                "manual_url": "http://google.com/",
                "anchor": "test",
                "mailto": "test@gmail.com",
                "phone": "112",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors, {"content_object": ["Url with this object already exists"]}
        )

    def test_url_form_create_url_with_invalid_content_type_and_content_object(self):
        form = UrlForm(
            {"internal_name": "Test Name", "site": self.default_site.id, "url_type": 99, "content_object": 99}
        )

        self.assertDictEqual(
            form.errors,
            {
                "url_type": [
                    "Select a valid choice. 99 is not one of the available choices."
                ],
                "content_object": [
                    "Object does not exist in a given content type id: {} and site: {}".format(
                        99, self.default_site
                    )
                ],
            },
        )

    def test_url_form_create_url_with_empty_content_object(self):
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.default_site.pk,
                "url_type": self.page_contenttype_id,
                "content_object": None,
            }
        )

        self.assertDictEqual(form.errors, {"content_object": ["Field is required"], })

    def test_plugin_returns_correct_url_for_type_on_update(self):
        """
        Get URL returns based on a series of if statements meaning without proper validation the incorrect value
        is returned if the content type was previously populated but has since been changed to a charfield url type
        - Create a url pointing to a page
        - Ensure get_url returns the correct url
        - Change it to a manual_url
        - Ensure that get_url returns the updated url
        """
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.site2.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page2.pk,
            }
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.get_url(instance.site), "//foo.com/en/test2/")

        form = UrlForm(
            {
                "internal_name": "Test Name",
                "url": self.url.id,
                "site": self.site2.id,
                "url_type": "manual_url",
                "manual_url": "https://www.github.com"
            }
        )

        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.get_url(instance.site), "https://www.github.com")

    def test_get_url_change_to_page(self):
        manual_url = "https://example.com/"
        url = self._create_url(manual_url=manual_url)

        self.assertEqual(url.get_url(url.site), manual_url)

        url.content_object = self.page
        url.save()
        parsed = urlparse(url.get_url(url.site))

        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/en/test/")

    def test_get_url_change_content_type(self):
        """
        Ensure get_url returns the correct url when a content type is changed from one to another using URlForm
        The issue was present previously as the getter for URL would assume that the form was setting the Generic
        Foreign Key to None!
        """
        # Create a URL with content type page
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.site2.id,
                "url_type": self.page_contenttype_id,
                "content_object": self.page2.pk,
            }
        )

        # Confirm the form is valid
        self.assertTrue(form.is_valid())

        # Save the form the create a model instance
        instance = form.save()

        # Ensure the correct url is being returned
        self.assertEqual(instance.get_url(instance.site), "//foo.com/en/test2/")

        # Create a form to update the model with a new content type
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "url": instance.pk,
                "site": self.site2.id,
                "url_type": self.poll_content_contenttype_id,
                "content_object": self.poll_content.pk,
            }
        )

        # Ensure form is valid
        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.get_url(instance.site), "//foo.com/en/admin/polls/pollcontent/")

    def test_url_basic_type_change(self):
        """
        Test that get_url returns the correct url when a content type is change from a basic type to a content object,
        and vice-versa
        """
        # Create a URL form targeting a manual url
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.site2.id,
                "url_type": "manual_url",
                "manual_url": "https://www.example.com",
                "content_object": None,
            }
        )

        # Confirm the form is valid
        self.assertTrue(form.is_valid())

        # Save the form the create a model instance
        instance = form.save()

        # Ensure the correct url is being returned
        self.assertEqual(instance.get_url(instance.site), "https://www.example.com")

        # Create a new form to set the URL to use a Generic FK
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "url": instance.pk,
                "site": self.site2.id,
                "url_type": self.poll_content_contenttype_id,
                "content_object": self.poll_content.pk,
            }
        )

        # Ensure form is valid
        self.assertTrue(form.is_valid())

        # Save the form
        instance = form.save()

        self.assertEqual(instance.get_url(instance.site), "//foo.com/en/admin/polls/pollcontent/")

        # Create a URL form targeting a manual url again
        form = UrlForm(
            {
                "internal_name": "Test Name",
                "site": self.site2.id,
                "url_type": "manual_url",
                "manual_url": "https://www.example.com",
                "content_object": None,
            }
        )

        # Ensure form is valid
        self.assertTrue(form.is_valid())

        # Save the form the create a model instance
        instance = form.save()

        # Ensure the correct url is being returned after change
        self.assertEqual(instance.get_url(instance.site), "https://www.example.com")
