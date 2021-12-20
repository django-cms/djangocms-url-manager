(function($) {
    $(function() {
        function initializeSiteWidget($element) {
            $element.select2({
                allowClear: true
            });
        }
        function initializeUrlWidget($element) {
            let endpoint = $element.attr('data-select2-url');
            let itemsPerPage = 30;

            $element.select2({
                ajax: {
                    url: endpoint,
                    dataType: 'json',
                    quietMillis: 250,
                    data: function(term, page) {
                        return {
                            page: page,
                            limit: itemsPerPage,
                            site: $(this.context)
                                .closest('fieldset')
                                .find('.field-site select')
                                .val(),
                        };
                    },
                    results: function(data, page) {
                        return data;
                    }
                },
                initSelection: function(element, callback) {
                    var objectId = element.val();
                    $.ajax({
                        url: endpoint,
                        dataType: 'json',
                        data: {
                            pk: objectId,
                        }
                    })
                        .done(function(data) {
                            var text = objectId;
                            if (data.results.length) {
                                text = data.results[0].text;
                            }
                            callback({ id: objectId, text: text });
                        })
                        .fail(function() {
                            callback({ id: objectId, text: objectId });
                        });
                }
            });
        }
        $(':not([id*=__prefix__])[id$="site"]').each(function(i, element) {
            initializeSiteWidget($(element));
        });
        $(':not([id*=__prefix__])[id$="url_grouper"]').each(function(i, element) {
            initializeUrlWidget($(element));
        });
        django
            .jQuery(document)
    });
})(CMS.$);
