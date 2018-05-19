from django.conf.urls import url

from . import constants, views


urlpatterns = [
    url(
        r'^select2/$',
        views.PageSelect2View.as_view(),
        name=constants.SELECT2_PAGE_URL_NAME,
    ),
]
