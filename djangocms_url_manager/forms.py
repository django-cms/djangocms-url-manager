from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from cms.utils.urlutils import admin_reverse

from .constants import SELECT2_CONTENT_TYPE_OBJECT_URL_NAME, SELECT2_URLS
from .models import BASIC_TYPE_CHOICES, LinkPlugin, Url, UrlOverride
from .utils import supported_models


class Select2Mixin:
    class Media:
        css = {"all": ("cms/js/select2/select2.css",)}
        js = ("cms/js/select2/select2.js", "djangocms_url_manager/js/create_url.js")


class SiteSelectWidget(Select2Mixin, forms.Select):
    pass


class UrlTypeSelectWidget(Select2Mixin, forms.Select):
    pass


class ContentTypeObjectSelectWidget(Select2Mixin, forms.TextInput):
    def get_url(self):
        return admin_reverse(SELECT2_CONTENT_TYPE_OBJECT_URL_NAME)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault("data-select2-url", self.get_url())
        return attrs


class UrlSelectWidget(Select2Mixin, forms.Select):
    pass


class HtmlLinkMixin:
    class Media:
        css = {"all": ("cms/js/select2/select2.css",)}
        js = ("cms/js/select2/select2.js", "djangocms_url_manager/js/html_link.js")


class HtmlLinkSiteSelectWidget(HtmlLinkMixin, forms.Select):
    pass


class HtmlLinkUrlSelectWidget(Select2Mixin, forms.TextInput):
    def get_url(self):
        return admin_reverse(SELECT2_URLS)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault("data-select2-url", self.get_url())
        return attrs


class UrlForm(forms.ModelForm):

    url_type = forms.ChoiceField(
        label=_("Type"), widget=UrlTypeSelectWidget(attrs={"data-placeholder": _("Select type")})
    )
    site = forms.ModelChoiceField(
        label=_("Site"),
        queryset=Site.objects.all(),
        widget=SiteSelectWidget(attrs={"data-placeholder": _("Select site")}),
        empty_label="",
    )
    content_object = forms.CharField(
        label=_("Content object"),
        widget=ContentTypeObjectSelectWidget(attrs={"data-placeholder": _("Select content object")}),
        required=False,
    )

    class Meta:
        model = Url
        fields = ("internal_name", "url_type", "site", "content_object", "manual_url", "anchor", "mailto", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set choices based on setup models for type field
        choices = []
        for model in supported_models():
            choices.append((ContentType.objects.get_for_model(model).id, model._meta.verbose_name.capitalize()))
        # Add basic options for type field.
        choices += BASIC_TYPE_CHOICES
        self.fields["url_type"].choices = choices

        # Set type if object exists
        if self.instance:
            if self.instance.content_type_id:
                self.fields["url_type"].initial = self.instance.content_type_id
                self.fields["content_object"].initial = self.instance.object_id
            else:
                for type_name in dict(BASIC_TYPE_CHOICES).keys():
                    if getattr(self.instance, type_name):
                        self.fields["url_type"].initial = type_name
                        break

    def clean(self):
        data = super().clean()
        url_type = data.get("url_type")
        content_object = data.get("content_object")
        is_basic_type = url_type in dict(BASIC_TYPE_CHOICES).keys()

        for type_name in dict(BASIC_TYPE_CHOICES).keys():
            if type_name != url_type:
                data[type_name] = ""

        if is_basic_type:
            if url_type not in self.errors and not data[url_type]:
                self.add_error(url_type, _("Field is required"))
        elif content_object:
            site = data.get("site")
            try:
                content_type = ContentType.objects.get_for_id(url_type)
                model = content_type.model_class()
                content_object_qs = model.objects.all()
                if hasattr(model.objects, "on_site"):
                    content_object_qs = content_object_qs.on_site(site)
                elif hasattr(model, "site"):
                    content_object_qs = content_object_qs.filter(site=site)
                content_object = content_object_qs.get(pk=int(content_object))

                if (
                    # dont validate for UrlOverride
                    not data.get("url")
                    and Url.objects.filter(content_type=content_type, object_id=data["content_object"]).exists()
                ):
                    self.add_error("content_object", _("Url with this object already exists"))

                data["content_object"] = content_object
            except ObjectDoesNotExist:
                self.add_error(
                    "content_object",
                    _(
                        "Object does not exist in a given content type id: {} and site: {}".format(
                            # url_type from cleaned_data can be None when it dont
                            # pass validation
                            self.data["url_type"],
                            site,
                        )
                    ),
                )
        else:
            self.add_error("content_object", _("Field is required"))
        return data

    def clean_anchor(self):
        anchor = self.cleaned_data.get("anchor")

        if anchor and anchor[0] == "#":
            self.add_error("anchor", _('Do not include a preceding "#" symbol.'))
        return anchor

    def save(self, **kwargs):
        url_type = self.cleaned_data.get("url_type")
        is_basic_type = url_type in dict(BASIC_TYPE_CHOICES).keys()
        if not is_basic_type:
            self.instance.content_object = self.cleaned_data["content_object"]
        return super().save(**kwargs)


class UrlOverrideForm(UrlForm):
    class Meta:
        model = UrlOverride
        fields = ("url",) + UrlForm.Meta.fields

    def clean(self):
        data = super().clean()
        url = data.get("url")
        site = data.get("site")

        if url and url.site == site:
            raise forms.ValidationError(
                {"site": _("Overriden site must be different from the original.")}  # noqa: E501
            )
        return data


class HtmlLinkForm(forms.ModelForm):

    site = forms.ModelChoiceField(
        label=_("Site"),
        queryset=Site.objects.all(),
        widget=HtmlLinkSiteSelectWidget(attrs={"data-placeholder": _("Select site")}),
        required=False,
    )

    url = forms.CharField(
        label=_("Url"), widget=HtmlLinkUrlSelectWidget(attrs={"data-placeholder": _("Select URL object from list")})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set url if object exists
        if self.instance and self.instance.url_id:
            self.fields["url"].initial = self.instance.url_id

    class Meta:
        model = LinkPlugin
        fields = ("internal_name", "site", "url", "label", "template", "target", "attributes")

    def clean(self):
        data = super().clean()
        try:
            data["url"] = Url.objects.get(pk=int(data["url"]))
        except ValueError:
            self.add_error("url", _("Invalid value"))
        except ObjectDoesNotExist:
            self.add_error("url", _("Url does not exist"))
        return data
