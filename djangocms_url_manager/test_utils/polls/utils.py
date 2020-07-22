def get_all_poll_content_objects(model, **kwargs):
    return model.objects.all()


def get_published_pages_objects(model, site, **kwargs):
    return model.objects.published(site).filter(publisher_is_draft=False)


def get_poll_search_results(model, content_type_model, url_model, queryset, search_term):
    """
    A helper method to filter across generic foreign key relations.
    Provide additional helpers for any models when extending this app.
    :param model: The supported model
    :param queryset: The queryset to be filtered
    :param search_term: Term to be searched for
    :return: results
    """
    poll_content_queryset = model.objects.filter(title__icontains=search_term)
    content_type_id = content_type_model.objects.get_for_model(model).id

    for poll_content in poll_content_queryset:
        try:
            queryset |= url_model.objects.filter(
                object_id=poll_content.page.id,
                content_type=content_type_id
            )
        except BaseException:
            pass

    return queryset
