(function($) {

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

    $(document).ready(function() {
        var orderableChangelistField = $('#js-orderable-changelist-field').val();
        if (orderableChangelistField) {
            initOrderableChangelist(orderableChangelistField)
        }
    });

})(jQuery);
