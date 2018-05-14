(function($) {
    $(function() {
        function initializeSiteWidget($element) {
            $element.select2({
                allowClear: true
            });
        }
        function initializePageWidget($element) {
            var pageEndpoint = $element.attr('data-select2-url');
            var itemsPerPage = 30;
            $element.select2({
                ajax: {
                    url: pageEndpoint,
                    dataType: 'json',
                    quietMillis: 250,
                    data: function(term, page) {
                        return {
                            term: term,
                            page: page,
                            limit: itemsPerPage,
                            site: $(this.context).closest('fieldset').find('.field-site select').val()
                        };
                    },
                    results: function(data, page) {
                        return data;
                    }
                },
                initSelection: function(element, callback) {
                    var pageId = element.val();
                    $.ajax({
                        url: pageEndpoint,
                        dataType: 'json',
                        data: {
                            pk: pageId
                        }
                    })
                        .done(function(data) {
                            var text = pageId;
                            if (data.results.length) {
                                text = data.results[0].text;
                            }
                            callback({ id: pageId, text: text });
                        })
                        .fail(function() {
                            callback({ id: pageId, text: pageId });
                        });
                }
            });
        }
        initializeSiteWidget($('#id_site'));
        initializePageWidget($('#id_page'));
        django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
            initializeSiteWidget($($row).find('select[id$="site"]'));
            initializePageWidget($($row).find('input[id$="page"]'));
        });
    });
})(CMS.$);
