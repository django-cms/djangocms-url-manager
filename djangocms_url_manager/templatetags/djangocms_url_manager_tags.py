from django import template

from cms.toolbar.utils import get_toolbar_from_request


register = template.Library()


@register.simple_tag(takes_context=True)
def render_url(context, instance):
    request = context["request"]
    toolbar = get_toolbar_from_request(request)

    # Are we in an editable mode?
    show_draft_content = False
    if toolbar.edit_mode_active or toolbar.preview_mode_active:
        show_draft_content = True

    url = instance.get_content(show_draft_content)

    if not url:
        return ""
    renderer = toolbar.get_content_renderer()
    return url.get_url(renderer.current_site)
