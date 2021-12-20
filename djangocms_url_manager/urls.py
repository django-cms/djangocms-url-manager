from django.urls import re_path

from . import constants, views


urlpatterns = [
    re_path(
        r"^select2/$",
        views.ContentTypeObjectSelect2View.as_view(),
        name=constants.SELECT2_CONTENT_TYPE_OBJECT_URL_NAME,
    ),
    re_path(
        r"^select2/urls/$", views.UrlSelect2View.as_view(), name=constants.SELECT2_URLS
    ),
]
