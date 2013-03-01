import urllib

from django import forms
from django.contrib.admin.filters import FieldListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.util import prepare_lookup_value
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _


class FormListFilter(FieldListFilter):
    template = 'stratus/filters/form.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field = field
        self.field_path = field_path
        self.title = getattr(field, 'verbose_name', field_path)
        self.fields = self._get_fields()

        super(FieldListFilter, self).__init__(request, params, model, model_admin)

        for lookup, field in self.fields.iteritems():
            if lookup in params:
                value = params.pop(lookup)
                if value:
                    self.used_parameters[lookup] = prepare_lookup_value(lookup, value)

        form_data = {}
        action_data = {}
        for key, value in request.GET.iteritems():
            if key in self.fields:
                form_data[key] = value
            else:
                action_data[key] = value

        self.action = '%s?%s' % (request.path, urllib.urlencode(action_data))
        self.form = self.get_form()(data=form_data or None)

        self.media = self.get_media()

    def choices(self, cl):
        return []

    def _get_fields(self):
        return SortedDict(('%s__%s' % (self.field_path, lookup), field)
            for lookup, field in self.get_fields())

    def get_fields(self):
        return []

    def get_form(self):
        return type('%sForm' % self.__class__.__name__, (forms.Form,), self.fields)

    def get_media(self):
        return self.form.media


class DateRangeListFilter(FormListFilter):

    def get_fields(self):
        return [
            ('lte', forms.DateField(label=_('Start'), widget=AdminDateWidget)),
            ('gte', forms.DateField(label=_('End'), widget=AdminDateWidget)),
        ]

    def get_media(self):
        media = forms.Media(
            css={'all': ['admin/css/widgets.css']},
            js=['stratus/js/calendarbox.js'],
        )
        return super(DateRangeListFilter, self).get_media() + media
