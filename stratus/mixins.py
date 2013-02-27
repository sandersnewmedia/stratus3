from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import FieldDoesNotExist


class OrderableMixin(object):
    change_list_template = 'stratus/orderable_change_list.html'
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
        super(OrderableMixin, self).__init__(model, admin_site)
        if self.orderable_field:
            try:
                model._meta.get_field_by_name(self.orderable_field)[0]
            except FieldDoesNotExist:
                raise ImproperlyConfigured("%s has no orderable field named "
                    "'%s'" % (model.__name__, self.orderable_field))

            if self.orderable_field not in self.list_display:
                self.list_display = list(self.list_display) + [self.orderable_field]

            if self.orderable_field not in self.list_editable:
                self.list_editable = list(self.list_editable) + [self.orderable_field]

            self.ordering = [self.orderable_field]
