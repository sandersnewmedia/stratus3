from functools import update_wrapper

from django.contrib import admin
from django.http import HttpResponse
from django.utils import simplejson


class OrderableMixin(object):
    ordering_field = None

    class Media(object):
        js = ['stratus/js/jquery.ui.js']

    def __init__(self, *args, **kwargs):
        if self.ordering_field and not self.ordering:
            self.ordering = [self.ordering_field]
        super(OrderableMixin, self).__init__(*args, **kwargs)


class OrderableAdmin(OrderableMixin, admin.ModelAdmin):
    change_list_template = 'admin/orderable_change_list.html'

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^reorder/$', wrap(self.reorder_view), name='%s_%s_reorder' % info),
        )

        return urlpatterns + super(OrderableAdmin, self).get_urls()

    def reorder_view(self, request):
        if self.ordering_field:
            data = {}
            for i, pk in enumerate(request.POST.get('pks', '').split(',')):
                order = i + 1
                obj = self.get_object(request, pk)
                setattr(obj, self.ordering_field, order)
                obj.save()
                data[pk] = order
        return HttpResponse(simplejson.dumps(data), content_type='application/json')


class OrderableTabularInline(OrderableMixin, admin.TabularInline):
    template = 'admin/edit_inline/orderable_tabular.html'
