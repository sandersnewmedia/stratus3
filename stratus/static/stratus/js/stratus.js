(function($) {

    $(document).ready(function() {
        $('.js-delete .btn').on('click', function() {
            var button = $(this);
            var checkbox = button.parent().find('input');
            checkbox.prop('checked', !checkbox.prop('checked'));
            button.text(checkbox.prop('checked') ? button.data('on-text') :  button.data('off-text'));
            return false;
        });
    });

})(jQuery);
