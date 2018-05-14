from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_attributes_field.fields import AttributesField

from cms.models import CMSPlugin, Page


__all__ = [
    'Url',
    'UrlPlugin',
]


# Add additional choices through the ``settings.py``.
TEMPLATE_DEFAULT = 'default'


def get_templates():
    choices = [
        (TEMPLATE_DEFAULT, _('Default')),
    ]
    choices += getattr(
        settings,
        'DJANGOCMS_URL_MANAGER_TEMPLATES',
        [],
    )
    return choices


TARGET_CHOICES = (
    ('_blank', _('Open in new window')),
    ('_self', _('Open in same window')),
    ('_parent', _('Delegate to parent')),
    ('_top', _('Delegate to top')),
)


class AbstractUrl(models.Model):
    site = models.ForeignKey(Site)
    manual_url = models.URLField(
        verbose_name=_('manual URL'),
        blank=True,
        max_length=2040,
        help_text=_('Provide a valid URL to an external website.'),
    )
    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    anchor = models.CharField(
        verbose_name=_('anchor'),
        blank=True,
        max_length=255,
        help_text=_('Appends the value only after the internal or external link. '  # noqa: E501
                    'Do <em>not</em> include a preceding "#" symbol.'),
    )
    mailto = models.EmailField(
        verbose_name=_('email address'),
        blank=True,
        max_length=255,
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        blank=True,
        max_length=255,
    )

    def get_url(self):
        if self.page:
            url = '//{}{}'.format(
                self.site.domain,
                self.page.get_absolute_url(),
            )
        elif self.manual_url:
            url = self.manual_url
        elif self.phone:
            url = 'tel:{}'.format(self.phone.replace(' ', ''))
        elif self.mailto:
            url = 'mailto:{}'.format(self.mailto)
        else:
            url = ''
        if (not self.phone and not self.mailto) and self.anchor:
            url += '#{}'.format(self.anchor)

        return url

    class Meta:
        abstract = True


class Url(AbstractUrl):
    label = models.CharField(
        verbose_name=_('label'),
        max_length=120,
    )

    class Meta:
        verbose_name = _('url')
        verbose_name_plural = _('urls')

    def __str__(self):
        return self.label


class UrlOverride(AbstractUrl):
    url = models.ForeignKey(
        Url,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('url override')
        verbose_name_plural = _('url overrides')


class UrlPlugin(CMSPlugin):
    url = models.ForeignKey(
        Url,
        verbose_name=_('url'),
        related_name='cms_plugins',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=120,
    )
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=TEMPLATE_DEFAULT,
        max_length=255,
    )
    target = models.CharField(
        verbose_name=_('Target'),
        choices=TARGET_CHOICES,
        blank=True,
        max_length=255,
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['href', 'target'],
    )

    class Meta:
        verbose_name = _('url plugin model')
        verbose_name_plural = _('url plugin models')

    def __str__(self):
        return self.name
