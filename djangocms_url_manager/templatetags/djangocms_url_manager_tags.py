from django import template

from cms.toolbar.utils import get_toolbar_from_request


register = template.Library()


@register.simple_tag(takes_context=True)
def render_url(context, instance):
    request = context["request"]
    toolbar = get_toolbar_from_request(request)
    renderer = toolbar.get_content_renderer()
    return instance.get_url(renderer.current_site)
