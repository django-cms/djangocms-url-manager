from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import ListView

from djangocms_url_manager.utils import is_model_supported


class ContentTypeObjectSelect2View(ListView):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        data = {
            'results': [
                {
                    'text': str(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list'] if str(obj)
            ],
            'more': context['page_obj'].has_next(),
        }
        return JsonResponse(data)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        content_id = self.request.GET.get('content_id', None)
        site = self.request.GET.get('site')

        try:
            content_object = ContentType.objects.get_for_id(content_id)
        except ContentType.DoesNotExist:
            raise ValueError(
                'Content type with id {} does not exists.'.format(content_id)
            )

        model = content_object.model_class()
        if not is_model_supported(model):
            raise ValueError(
                '{} is not available to use, check content_id param'.format(model)
            )

        queryset = model.objects.all()
        try:
            pk = int(self.request.GET.get('pk'))
        except (TypeError, ValueError):
            pk = None

        if site:
            if hasattr(model.objects, 'on_site'):
                queryset = queryset.on_site(site)
            elif hasattr(model, 'site'):
                queryset = queryset.filter(site=site)
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get('limit', 30)
