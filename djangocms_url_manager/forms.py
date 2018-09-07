from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from cms.utils.urlutils import admin_reverse

from djangocms_url_manager.utils import supported_models

from .constants import SELECT2_CONTENT_TYPE_OBJECT_URL_NAME
from .models import BASIC_TYPE_CHOICES, Url, UrlOverride


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


class TypeSelectWidget(Select2Mixin, forms.Select):
    pass


class ContentTypeObjectSelectWidget(Select2Mixin, forms.TextInput):

    def get_url(self):
        return admin_reverse(SELECT2_CONTENT_TYPE_OBJECT_URL_NAME)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('data-select2-url', self.get_url())
        return attrs


class UrlForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set choices based on setup models for type field
        choices = []
        for model in supported_models():
            choices.append((
                ContentType.objects.get_for_model(model).id,
                model._meta.verbose_name.capitalize(),
            ))

        # Add basic options for type field.
        choices += BASIC_TYPE_CHOICES

        self.fields['type_object'] = forms.ChoiceField(choices=choices)

        # Set type if object exists
        if self.instance:
            if self.instance.content_type_id:
                self.fields['type_object'].initial = self.instance.content_type_id
                self.fields['content_object'].initial = self.instance.object_id
            else:
                for type_name in dict(BASIC_TYPE_CHOICES).keys():
                    if getattr(self.instance, type_name):
                        self.fields['type_object'].initial = type_name

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

    type_object = forms.ChoiceField(
        label=_('Type'),
        widget=TypeSelectWidget(
            attrs={
                'data-placeholder': _('Select type'),
            },
        ),
    )

    content_object = forms.CharField(
        label=_('Content type object'),
        widget=ContentTypeObjectSelectWidget(
            attrs={
                'data-placeholder': _('Select content type object'),
            },
        ),
        required=False,
    )

    class Meta:
        model = Url
        fields = (
            'site', 'type_object', 'manual_url', 'anchor', 'mailto', 'phone',
        )

    def clean(self):
        data = self.cleaned_data
        type_object = data.get('type_object')
        content_object = data.get('content_object')
        is_base_type = type_object in dict(BASIC_TYPE_CHOICES).keys()

        if is_base_type:
            if type_object not in self.errors and not data[type_object]:
                self.add_error(type_object, 'Field is required')
        else:
            if content_object:
                try:
                    model = ContentType.objects.get_for_id(type_object).model_class()
                    model.objects.get(id=int(content_object))
                except ObjectDoesNotExist:
                    self.add_error('content_object', 'Object not exist in selected model')
            else:
                self.add_error('content_object', 'Field is required')

        return data

    def clean_anchor(self):
        anchor = self.cleaned_data.get('anchor')

        if anchor:
            if anchor[0] == '#':
                self.add_error('anchor', 'Do not include a preceding "#" symbol.')
        return anchor

    def save(self, commit=True):
        instance = super().save(commit=False)
        type_object = self.cleaned_data['type_object']

        for type_name in dict(BASIC_TYPE_CHOICES).keys():
            setattr(instance, type_name, '')

        instance.content_object = None

        if type_object in dict(BASIC_TYPE_CHOICES).keys():
            setattr(instance, type_object, self.cleaned_data[type_object])
        else:
            instance.content_type = ContentType.objects.get_for_id(int(type_object))
            instance.object_id = int(self.cleaned_data.get('content_object'))

        if commit:
            instance.save()
        return instance


class UrlOverrideForm(UrlForm):

    class Meta:
        model = UrlOverride
        fields = (
            'url', 'site', 'type_object', 'manual_url', 'anchor', 'mailto', 'phone',
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
