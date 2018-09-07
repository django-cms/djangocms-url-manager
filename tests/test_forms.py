from unittest import skipIf, skipUnless

from django.contrib.sites.models import Site

from djangocms_url_manager.compat import CMS_36
from djangocms_url_manager.forms import (
    ContentTypeObjectSelectWidget,
    UrlForm,
    UrlOverrideForm,
)

from .base import BaseUrlTestCase


class UrlManagerFormsTestCase(BaseUrlTestCase):

    def test_url_override_form(self):
        site3 = Site.objects.create(
            name='bar.com',
            domain='bar.com',
        )
        form = UrlOverrideForm({
            'url': self.url.pk,
            'site': site3.pk,
            'type_object': 'manual_url',
            'manual_url': 'http://google.com/'
        }).save()
        self.assertEqual(form.site_id, site3.pk),
        self.assertEqual(form.manual_url, 'http://google.com/'),
        self.assertEqual(form.content_type_id, None),
        self.assertEqual(form.object_id, None),
        self.assertEqual(form.anchor, ''),
        self.assertEqual(form.mailto, ''),
        self.assertEqual(form.phone, ''),
        self.assertEqual(form.url_id, 1),

    def test_url_override_form_disallow_same_site_as_original_url(self):
        form = UrlOverrideForm({
            'url': self.url.pk,
            'site': self.url.site_id,
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                'type_object': ['This field is required.'],
                'content_object': ['Field is required'],
                'site': ['Overriden site must be different from the original.']
            }
        )

    def test_data_select_widget_build_attrs(self):
        self.assertDictContainsSubset(
            ContentTypeObjectSelectWidget().build_attrs({}),
            {'data-select2-url': self.select2_endpoint},
        )

    def test_url_form_empty_data(self):
        form = UrlForm({
            'site': self.default_site,
        })
        self.assertFalse(form.is_valid())

    @skipUnless(CMS_36, "CMS<4.0")
    def test_url_form_type_object_choices_for_cms36(self):
        form = UrlForm()
        self.assertListEqual(
            form.fields['type_object'].choices,
            [
                (28, 'Poll content'),
                (2, 'Page'),
                (30, 'Blog content'),
                ('manual_url', 'Manual URL'),
                ('anchor', 'Anchor'),
                ('mailto', 'Email address'),
                ('phone', 'Phone')
            ]
        )

    @skipIf(CMS_36, "CMS<4.0")
    def test_url_form_type_object_choices_for_cms40(self):
        form = UrlForm()
        self.assertListEqual(
            form.fields['type_object'].choices,
            [
                (29, 'Poll content'),
                (2, 'Page'),
                (31, 'Blog content'),
                ('manual_url', 'Manual URL'),
                ('anchor', 'Anchor'),
                ('mailto', 'Email address'),
                ('phone', 'Phone')
            ]
        )

    def test_url_form_create_url_with_valid_manual_url(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'manual_url',
            'manual_url': 'https://google.com/',
            'anchor': 'test',
            'mailto': 'test@gmail.com',
            'phone': '112',
            'content_object': self.page.id,
        }).save()
        self.assertEqual(form.site_id, self.default_site.id)
        self.assertEqual(form.manual_url, 'https://google.com/')
        self.assertEqual(form.anchor, '')
        self.assertEqual(form.mailto, '')
        self.assertEqual(form.phone, '')
        self.assertEqual(form.content_type_id, None)
        self.assertEqual(form.object_id, None)

    def test_url_form_create_url_with_invalid_manual_url(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'manual_url',
            'manual_url': 'google',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'manual_url': ['Enter a valid URL.']},
        )

    def test_url_form_create_url_with_empty_manual_url(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'manual_url',
            'manual_url': '',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'manual_url': ['Field is required']},
        )

    def test_url_form_create_url_with_valid_anchor(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'anchor',
            'anchor': 'test',
        }).save()
        self.assertEqual(form.anchor, 'test')

    def test_url_form_create_url_with_invalid_anchor(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'anchor',
            'anchor': '#example',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'anchor': ['Do not include a preceding "#" symbol.']},
        )

    def test_url_form_create_url_with_empty_anchor(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'anchor',
            'anchor': '',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'anchor': ['Field is required']},
        )

    def test_url_form_create_url_with_valid_mailto(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'mailto',
            'mailto': 'norman.burdett@gmail.com',
        }).save()
        self.assertEqual(form.mailto, 'norman.burdett@gmail.com')

    def test_url_form_create_url_with_invalid_mailto(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'mailto',
            'mailto': 'norman',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'mailto': ['Enter a valid email address.']},
        )

    def test_url_form_create_url_with_empty_mailto(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'mailto',
            'mailto': '',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'mailto': ['Field is required']},
        )

    def test_url_form_create_url_with_valid_phone(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'phone',
            'phone': '+44 20 7946 0916',
        }).save()
        self.assertEqual(form.phone, '+44 20 7946 0916')

    def test_url_form_create_url_with_empty_phone(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 'phone',
            'phone': '',
        })
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {'phone': ['Field is required']},
        )

    def test_url_form_create_url_with_valid_page_content_and_content_object(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': self.page_content_id,
            'content_object': self.page.id,
            'manual_url': 'http://google.com/',
            'anchor': 'test',
            'mailto': 'test@gmail.com',
            'phone': '112',
        }).save()
        self.assertEqual(form.site_id, self.default_site.id)
        self.assertEqual(form.content_type_id, self.page_content_id)
        self.assertEqual(form.object_id, self.page.id)
        self.assertEqual(form.manual_url, '')
        self.assertEqual(form.anchor, '')
        self.assertEqual(form.mailto, '')
        self.assertEqual(form.phone, '')

    def test_url_form_create_url_with_invalid_content_type_and_content_object(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': 99,
            'content_object': 99,
        })
        self.assertDictEqual(
            form.errors,
            {
                'type_object': ['Select a valid choice. 99 is not one of the available choices.'],
                'content_object': ['Object not exist in selected model']
            }
        )

    def test_url_form_create_url_with_empty_content_object(self):
        form = UrlForm({
            'site': self.default_site.id,
            'type_object': self.page_content_id,
            'content_object': None,
        })
        self.assertDictEqual(
            form.errors,
            {'content_object': ['Field is required']}
        )
