(function($) {

    var fields = [
        'single_line_text',
        'multiple_line_text',
        'html',
        'image',
    ];

    var inputSelector = $.map(fields, function(name) {
        return '[name*="content_' + name + '"]';
    }).join(',');

    var fieldSelector = $.map(fields, function(name) {
        return '.field-content_' + name;
    }).join(',');

    var contentSelector = '.field-content';

    var transferContent = function() {
        var field = $(this);
        field.parents('fieldset').find('.field-content textarea').val(field.val());
    };

    var trackPreChange = function() {
        $(this).data('preChangeValue', $(this).val());
    };

    var toggleFields = function(e) {
        var select = $(this)
        var fieldName = select.val();
        var previousFieldName = (select.data('preChangeValue') || fieldName);
        var fieldset = select.parents('fieldset');
        var changed = (previousFieldName != fieldName);
        var hasValue = $.trim(fieldset.find('[name*="content_' + previousFieldName + '"]').val()) != '';
        var message = 'Are you sure you want to change content types? You will lose whats current entered.';

        if (changed && hasValue) {
            if (confirm(message)) {
                fieldset.find(inputSelector).val('');
            } else {
                select.val(previousFieldName);
                return false;
            }
        }

        fieldset.find(fieldSelector).hide();
        fieldset.find('.field-content_' + fieldName).show();

        select.data('preChangeValue', fieldName);
    };

    $(document).ready(function() {
        $('.field-content_type select')
            .live('focus', trackPreChange)
            .live('change', toggleFields)
            .each(toggleFields);
        //$(contentSelector).hide();
    });

})(django.jQuery);
