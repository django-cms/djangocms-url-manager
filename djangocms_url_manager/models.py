from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.utils.i18n import get_default_language_for_site

from djangocms_attributes_field.fields import AttributesField

from djangocms_url_manager.utils import is_versioning_enabled


__all__ = ["Url", "LinkPlugin"]


# Add additional choices through the ``settings.py``.
TEMPLATE_DEFAULT = "default"


def get_templates():
    choices = [(TEMPLATE_DEFAULT, _("Default"))]
    choices += getattr(settings, "DJANGOCMS_URL_MANAGER_TEMPLATES", [])
    return choices


TARGET_CHOICES = (
    ("_blank", _("Open in new window")),
    ("_self", _("Open in same window")),
    ("_parent", _("Delegate to parent")),
    ("_top", _("Delegate to top")),
)

BASIC_TYPE_CHOICES = (
    ("manual_url", _("Manual URL")),
    ("relative_path", _("Relative path")),
    ("anchor", _("Anchor")),
    ("mailto", _("Email address")),
    ("phone", _("Phone")),
)


class AbstractUrl(models.Model):
    site = models.ForeignKey(
        Site,
        related_name="%(app_label)s_%(class)s_site",
        on_delete=models.PROTECT,
    )
    content_type = models.ForeignKey(
        ContentType,
        related_name="%(app_label)s_%(class)s_content_type",
        on_delete=models.PROTECT,
        null=True,
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    manual_url = models.URLField(
        verbose_name=_("manual URL"),
        blank=True,
        max_length=2040,
        help_text=_("Provide a valid URL to an external website."),
    )
    relative_path = models.CharField(
        verbose_name=_("relative path"),
        blank=True,
        max_length=2040,
        help_text=_("Provide a relative path to a web page or resource"),
    )
    anchor = models.CharField(
        verbose_name=_("anchor"),
        blank=True,
        max_length=255,
        help_text=_(
            "Appends the value only after the internal or external link. "  # noqa: E501
            'Do <em>not</em> include a preceding "#" symbol.'
        ),
    )
    mailto = models.EmailField(
        verbose_name=_("email address"), blank=True, max_length=255
    )
    phone = models.CharField(verbose_name=_("phone"), blank=True, max_length=255)

    class Meta:
        abstract = True


class AbstractUrlGrouper(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @cached_property
    def name(self):
        """Show alias name for current language"""
        return self.get_name() or ''

    def get_name(self):
        content = self.get_content(show_draft_content=True)
        name = getattr(content, 'internal_name', 'URL {}'.format(self.pk))
        if is_versioning_enabled() and content:
            from djangocms_versioning.constants import DRAFT
            version = content.versions.first()

            if version.state == DRAFT:
                return '{} (Not published)'.format(name)

        return name

    def get_content_queryset(self):
        raise NotImplementedError("Models implementing AbstractUrlGrouper should implement get_content_queryset")

    def get_content(self, show_draft_content=False):
        qs = self.get_content_queryset()

        if show_draft_content and is_versioning_enabled():
            from djangocms_versioning.constants import DRAFT, PUBLISHED
            from djangocms_versioning.helpers import remove_published_where

            # Ensure that we are getting the latest valid content, the top most version can become
            # archived with a previous version re-published
            qs = remove_published_where(qs)
            qs = qs.filter(Q(versions__state=DRAFT) | Q(versions__state=PUBLISHED)).order_by('-versions__created')
        return qs.first()


class UrlGrouper(AbstractUrlGrouper):
    def get_content_queryset(self):
        return Url._base_manager.filter(url_grouper=self)


class Url(AbstractUrl):
    internal_name = models.CharField(
        verbose_name=_("internal name"),
        max_length=255,
        help_text=_("Provide internal name for URL objects for searching purpose"),
    )
    url_grouper = models.ForeignKey(
        UrlGrouper,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_url_grouper',
        null=True
    )
    date_modified = models.DateTimeField(
        verbose_name=_("Date Modified"), auto_now=True
    )

    class Meta:
        verbose_name = _("url")
        verbose_name_plural = _("urls")

    def _get_url_obj(self, site):
        if self.site_id == site:
            obj = self
        else:
            try:
                obj = self.urloverride_set.get(site=site)
            except UrlOverride.DoesNotExist:
                obj = self
        return obj

    def get_url(self, site):
        """
        All fields in basic_types and supported_models should be exclusive or's, otherwise the value will be
        returned based on the order of the below method rather than the intended value.
        """
        obj = self._get_url_obj(site)
        language = get_default_language_for_site(obj.site)
        if obj.content_object:
            try:
                absolute_url = obj.content_object.get_absolute_url(language=language)
            except BaseException:
                absolute_url = obj.content_object.get_absolute_url()
            url = "//{}{}".format(
                obj.site.domain, absolute_url
            )
        elif obj.manual_url:
            url = obj.manual_url
        elif obj.relative_path:
            url = obj.relative_path
        elif obj.phone:
            url = "tel:{}".format(obj.phone.replace(" ", ""))
        elif obj.mailto:
            url = "mailto:{}".format(obj.mailto)
        else:
            url = ""
        if (not obj.phone and not obj.mailto) and obj.anchor:
            url += "#{}".format(obj.anchor)

        return url

    def __str__(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return self.get_url(self.site)


class UrlOverride(AbstractUrl):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    internal_name = models.CharField(
        verbose_name=_("internal name"), max_length=255,
    )

    class Meta:
        verbose_name = _("url override")
        verbose_name_plural = _("url overrides")
        unique_together = (("site", "url"),)


class LinkPlugin(CMSPlugin):
    url_grouper = models.ForeignKey(
        UrlGrouper,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_url_grouper',
        null=True
    )
    label = models.CharField(verbose_name=_("label"), max_length=120)
    template = models.CharField(
        verbose_name=_("Template"),
        choices=get_templates(),
        default=TEMPLATE_DEFAULT,
        max_length=255,
    )
    target = models.CharField(
        verbose_name=_("Target"), choices=TARGET_CHOICES, blank=True, max_length=255
    )
    attributes = AttributesField(
        verbose_name=_("Attributes"), blank=True, excluded_keys=["href", "target"]
    )

    class Meta:
        verbose_name = _("url plugin model")
        verbose_name_plural = _("url plugin models")

    def __str__(self):
        return self.label
