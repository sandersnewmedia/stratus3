(function($) {

var originalOpenCalendar = DateTimeShortcuts.openCalendar;
DateTimeShortcuts.openCalendar = function(num) {
    originalOpenCalendar(num);

    var box = $('#' + DateTimeShortcuts.calendarDivName1 + num);
    var link = $('#' + DateTimeShortcuts.calendarLinkName + num);

    box.css({'z-index': 1000, 'left': link.offset()['left'] - box.width()});
};

})(django.jQuery);
