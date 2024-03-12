from django.urls import path

from . import constants, views


urlpatterns = [
    path(
        "select2/",
        views.ContentTypeObjectSelect2View.as_view(),
        name=constants.SELECT2_CONTENT_TYPE_OBJECT_URL_NAME,
    ),
    path(
        "select2/urls/", views.UrlSelect2View.as_view(), name=constants.SELECT2_URLS
    ),
]
