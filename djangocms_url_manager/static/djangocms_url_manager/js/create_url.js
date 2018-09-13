(function($) {
    $(function() {
        function initializeSiteWidget($element) {
            $element.select2({
                allowClear: true
            });
        }
        function initializeTypeWidget($element) {
            $element.select2({
                allowClear: true
            });
            checkTypeField($element);
        }
        function initializeContentObjectWidget($element) {
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
                            content_id: $(this.context)
                                .closest('fieldset')
                                .find('.field-url_type select')
                                .val()
                        };
                    },
                    results: function(data, page) {
                        return data;
                    }
                },
                initSelection: function(element, callback) {
                    var objectId = element.val();
                    var contentId = element.closest('fieldset').find('select[id$="url_type"]').val();
                    $.ajax({
                        url: endpoint,
                        dataType: 'json',
                        data: {
                            pk: objectId,
                            content_id: contentId,
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
        function hideFields($element) {
            $element.closest('fieldset').find('.field-content_object').hide();
            $element.closest('fieldset').find('.field-manual_url').hide();
            $element.closest('fieldset').find('.field-anchor').hide();
            $element.closest('fieldset').find('.field-mailto').hide();
            $element.closest('fieldset').find('.field-phone').hide();
        }
        function checkTypeField($element) {
            hideFields($element);

            if (jQuery.isNumeric($element.val())) {
                $element.closest('fieldset').find('.field-content_object').css('display', 'block');
            } else {
                switch($element.val()) {
                    case "manual_url":
                        $element.closest('fieldset').find('.field-manual_url').show();
                        break;
                    case "anchor":
                        $element.closest('fieldset').find('.field-anchor').show();
                        break;
                    case "mailto":
                        $element.closest('fieldset').find('.field-mailto').show();
                        break;
                    case "phone":
                        $element.closest('fieldset').find('.field-phone').show();
                        break;
                }
            }
        }

        $(':not([id*=__prefix__])[id$="site"]').each(function(i, element) {
            initializeSiteWidget($(element));
        });
        $(':not([id*=__prefix__])[id$="url_type"]').each(function(i, element) {
            initializeTypeWidget($(element));
            $($(element)).change(function(){
                checkTypeField($(element));
            });
        });
        $(':not([id*=__prefix__])[id$="content_object"]').each(function(i, element) {
            initializeContentObjectWidget($(element));
        });
        django
            .jQuery(document)
            .on('formset:added', function(event, $row, formsetName) {
                let url_type = $($row).find('[id$="url_type"]');
                $(url_type).change(function(){
                    checkTypeField(url_type);
                });
                initializeTypeWidget(url_type);
                initializeSiteWidget($($row).find('[id$="site"]'));
                initializeContentObjectWidget($($row).find('[id$="content_object"]'));
            });
    });
})(CMS.$);
