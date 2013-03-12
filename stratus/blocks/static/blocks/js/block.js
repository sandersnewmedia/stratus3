(function($) {

    var fields = [
        'single_line_text',
        'multiple_line_text',
        'html',
        'image',
    ];

    var applyToFields = function(fieldset, callback) {
        $.each(fields, function(i, name) {
            var el = fieldset.find('[name*="content_' + name + '"]');
            callback.apply(el, [i, name]);
        });
    };

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
        var confirmFunc = confirm || function() { return true; };

        if (changed && hasValue) {
            if (confirmFunc(message)) {
                applyToFields(fieldset, function(i, name) {
                    $(this).val('');
                });
            } else {
                select.val(previousFieldName);
                return false;
            }
        }

        applyToFields(fieldset, function(i, name, selector) {
            if (name == fieldName) {
                $(this).parents('.row1, .row2').show();
            } else {
                $(this).parents('.row1, .row2').hide();
            }
        });

        select.data('preChangeValue', fieldName);
    };

    var reColorRows = function() {
        var row = $(this).parents('.row1, .row2');
        var fieldset = row.parents('fieldset');

        applyToFields(fieldset, function(i, name, selector) {
            if (row.hasClass('row1')) {
                $(this).parents('.row1, .row2').removeClass('row1').addClass('row2');
            } else {
                $(this).parents('.row1, .row2').removeClass('row2').addClass('row1');
            }
        });
    };

    var hideWhenReadOnly = function() {
        var fieldset = $(this).parents('fieldset');

        applyToFields(fieldset, function(i, name, selector) {
            $(this).parents('.row1, .row2').hide();
        });

        

        fieldset.find('[name*="content_' + $(this).text().toLowerCase().replace(/ /g, '_') + '"]').parents('.row1, .row2').show();
    };

    $(document).ready(function() {
        $('[name*="content_type"]')
            .live('focus', trackPreChange)
            .live('change', toggleFields)
            .each(toggleFields)
            .each(reColorRows);

        var readOnly = $('.controls span i').filter(function() {
            return $(this).parents('.control-group').find('.control-label').text() == 'content type:';
        });
        readOnly.each(hideWhenReadOnly);
    });

})(yawdadmin.jQuery);
