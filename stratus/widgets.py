from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime, AdminTimeWidget

from stratus.templatetags.stratus_static import static


class StratusAdminSplitDateTime(AdminSplitDateTime):

    def __init__(self, attrs=None):
        widgets = [StratusAdminDateWidget, StratusAdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)


class StratusAdminDateWidget(AdminDateWidget):

    @property
    def media(self):
        js = ['calendar.js', 'admin/DateTimeShortcuts.js']
        return forms.Media(js=[static('stratus/js/{}'.format(path)) for path in js])


class StratusAdminTimeWidget(AdminTimeWidget):

    @property
    def media(self):
        js = ['calendar.js', 'admin/DateTimeShortcuts.js']
        return forms.Media(js=[static('stratus/js/{}'.format(path)) for path in js])
