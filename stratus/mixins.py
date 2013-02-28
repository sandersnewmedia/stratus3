from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import FieldDoesNotExist


class BaseOrderableMixin(object):
    orderable_field = None

    class Media(object):
        css = {
            'all': ['stratus/css/orderable.css'],
        }

        js = [
            'stratus/js/jquery.js',
            'stratus/js/jquery.ui.js',
            'stratus/js/orderable.js',
        ]

    def __init__(self, model, admin_site):
        super(BaseOrderableMixin, self).__init__(model, admin_site)
        if self.orderable_field:
            try:
                model._meta.get_field_by_name(self.orderable_field)[0]
            except FieldDoesNotExist:
                raise ImproperlyConfigured("%s has no orderable field named "
                    "'%s'" % (model.__name__, self.orderable_field))

            self.ordering = [self.orderable_field]


class OrderableAdminMixin(BaseOrderableMixin):
    change_list_template = 'stratus/orderable_change_list.html'

    def __init__(self, model, admin_site):
        super(OrderableAdminMixin, self).__init__(model, admin_site)
        if self.orderable_field:
            if self.orderable_field not in self.list_display:
                self.list_display = list(self.list_display) + [self.orderable_field]

            if self.orderable_field not in self.list_editable:
                self.list_editable = list(self.list_editable) + [self.orderable_field]


class BaseOrderableInlineMixin(BaseOrderableMixin):

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(BaseOrderableInlineMixin, self).get_formset(request, obj, **kwargs)
        formset.orderable_field = self.orderable_field
        return formset


class OrderableStackedInlineMixin(BaseOrderableInlineMixin):
    template = 'stratus/edit_inline/orderable_stacked.html'


class OrderableTabularInlineMixin(BaseOrderableInlineMixin):
    template = 'stratus/edit_inline/orderable_tabular.html'
