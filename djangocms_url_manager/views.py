from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from cms.models import Page
from .compat import CMS_36

from .compat import CMS_36


class PageSelect2View(ListView):
    if CMS_36:
        queryset = Page.objects.drafts()
    else:
        queryset = Page.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        data = {
            'results': [
                {
                    'text': str(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
            ],
            'more': context['page_obj'].has_next(),
        }
        return JsonResponse(data)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.GET.get('term')
        site = self.request.GET.get('site')
        try:
            pk = int(self.request.GET.get('pk'))
        except (TypeError, ValueError):
            pk = None
        q = Q()
        if term:
            q |= Q(title_set__title__icontains=term)
        if site:
            queryset = queryset.on_site(site)
        if pk:
            q |= Q(pk=pk)
        return queryset.filter(q)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('limit', 30)
