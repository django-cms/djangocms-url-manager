from django.template.response import TemplateResponse


def render_url(request, url):
    template = 'djangocms_url_manager/admin/preview.html'
    context = {'url': url}
    return TemplateResponse(request, template, context)
