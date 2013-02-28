(function($) {

    var toTitleCase = function(str) {
        return str.replace(/\w\S*/g, function(txt){
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    var initOrderableChangelist = function(field) {
        $('#result_list thead tr').prepend('<th>');
        $('#result_list tbody tr').prepend('<td class="orderable-handle"><span>Move</span></a>');
        $('#result_list tbody').sortable({
            items: 'tr',
            handle: '.orderable-handle',
            containment: 'tbody',
            update: function(event, ui) {
                var rows = $(this).find('tr');

                rows.each(function(i) {
                    var row = $(this);
                    var order = row.find('input[name$="-' + field + '"]');
                    var currentValue = order.val();
                    var newValue = i + 1;

                    if (currentValue != newValue) {
                        row.addClass('orderable-updated');
                        order.val(newValue);
                    }
                });

                rows.filter(':odd').addClass('row2').removeClass('row1');
                rows.filter(':even').addClass('row1').removeClass('row2');
            }
        });
    };

    var initOrderableStackedInline = function(inline) {
        var field = inline.data('orderable-field');

        inline.find('.inline-group').sortable({
            handle: 'h3',
            containment: '.inline-group',
            update: function(event, ui) {
                inline.find('.inline-related').each(function (i) {
                    $(this).find('input[name$="-' + field + '"]').val(i + 1);
                });
            }
        });
    };

    var initOrderableTabularInline = function(inline) {
        var field = inline.data('orderable-field');

        inline.find('th:contains(' + toTitleCase(field) + ')').hide();
        inline.find('input[name$="-' + field + '"]').hide();

        inline.find('tbody').sortable({
            update: function (event, ui) {
                var rows = inline.find('tbody tr');

                rows.each(function (i) {
                    $(this).find('input[name$="-' + field + '"]').val(i + 1);
                });

                rows.filter(':even').addClass('row1').removeClass('row2');
                rows.filter(':odd').addClass('row2').removeClass('row1');
            }
        });
    };

    $(document).ready(function() {
        var orderableChangelistField = $('#js-orderable-changelist-field').val();
        if (orderableChangelistField) {
            initOrderableChangelist(orderableChangelistField)
        }

        $('.js-orderable-tabular-inline').each(function() {
            initOrderableTabularInline($(this));
        });

        $('.js-orderable-stacked-inline').each(function() {
            initOrderableStackedInline($(this));
        });
    });

})(jQuery);
