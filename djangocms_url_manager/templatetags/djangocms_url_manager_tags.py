from django import template

from cms.toolbar.utils import get_toolbar_from_request


register = template.Library()


@register.simple_tag(takes_context=True)
def render_url(context, instance):
    request = context["request"]
    toolbar = get_toolbar_from_request(request)
    url = instance.get_content(toolbar.preview_mode_active)
    renderer = toolbar.get_content_renderer()
    return url.get_url(renderer.current_site) or ""
