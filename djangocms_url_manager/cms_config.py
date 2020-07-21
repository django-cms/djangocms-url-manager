from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page, PageContent

from djangocms_url_manager.utils import parse_settings

from .models import Url


class UrlCMSAppConfig(CMSAppConfig):
    djangocms_url_manager_enabled = True
    url_manager_supported_models = [Page]
    djangocms_navigation_enabled = getattr(
        settings, "DJANGOCMS_NAVIGATION_CMS_MODELS_ENABLED", False
    )
    navigation_models = {Url: ["internal_name"]}

    def get_page_search_results(self, model, queryset, search_term):
        """
        A helper method to filter across generic foreign key relations.
        Provide additional helpers for any models when extending this app.
        :param model: The supported model
        :param queryset: The queryset to be filtered
        :param search_term: Term to be searched for
        :return: results
        """
        page_content_queryset = PageContent.objects.filter(title__icontains=search_term)
        content_type_id = ContentType.objects.get_for_model(model).id

        for page_content in page_content_queryset:
            try:
                queryset |= Url.objects.filter(
                    object_id=page_content.page.id,
                    content_type=content_type_id
                )
            except BaseException:
                pass

        return queryset

    url_manager_supported_models_search_helpers = [
        {Page: get_page_search_results},
    ]


class UrlManagerCMSExtension(CMSAppExtension):
    def __init__(self):
        self.url_manager_supported_models = {}

    def handle_url_manager_setting(self, cms_config):
        """Check the url_manager_supported_models settings has been correctly set
        and add it to the masterlist
        """
        self.url_manager_supported_models = parse_settings(
            cms_config, "url_manager_supported_models"
        )

    def configure_app(self, cms_config):
        self.handle_url_manager_setting(cms_config)
