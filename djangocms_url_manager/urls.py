from django.conf.urls import url

from . import constants, views


urlpatterns = [
    url(
        r"^select2/$", views.ContentTypeObjectSelect2View.as_view(), name=constants.SELECT2_CONTENT_TYPE_OBJECT_URL_NAME
    ),
    url(r"^select2/urls/$", views.UrlSelect2View.as_view(), name=constants.SELECT2_URLS),
]
