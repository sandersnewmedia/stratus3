from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin.util import unquote
from django.http import HttpResponse, Http404
from django.utils import simplejson


class OrderableAdmin(admin.ModelAdmin):
    change_list_template = 'admin/orderable_change_list.html'
    ordering_field = None

    class Media(object):
        js = ['stratus/js/jquery.ui.js']

    def __init__(self, *args, **kwargs):
        if self.ordering_field and not self.ordering:
            self.ordering = [self.ordering_field]
        super(OrderableAdmin, self).__init__(*args, **kwargs)

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


class ImageGalleryAdmin(admin.ModelAdmin):
    add_form_template = 'admin/change_form.html'
    change_form_template = 'admin/imagegallery_change_form.html'

    class Media(object):
        js = [
            'stratus/js/jquery.js',
            'stratus/js/jquery.ui.js',
            'stratus/js/jquery.fileupload.js',
            'stratus/js/underscore.js',
            'stratus/js/backbone.js',
            'stratus/js/imagegallery.js',
        ]

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^(.+)/images/$', wrap(self.image_list_view), name='%s_%s_image_list' % info),
            url(r'^(.+)/images/(.+)/$', wrap(self.image_detail_view), name='%s_%s_image_detail' % info),
        )

        return urlpatterns + super(ImageGalleryAdmin, self).get_urls()

    def image_list_view(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))

        if request.method == 'GET':
            data, status = self.handle_image_list(request, obj)
        elif request.method == 'POST' and request.FILES:
            data, status = self.handle_image_create(request, obj)
        elif request.method == 'PUT':
            data, status = self.handle_image_update(request, obj)
        else:
            data, status = {}, 500

        return HttpResponse(simplejson.dumps(data), status=status, content_type='application/json')

    def image_detail_view(self, request, object_id, image_id):
        obj = self.get_object(request, unquote(object_id))
        try:
            image = obj.images.get(pk=image_id)
        except obj.images.model.DoesNotExist:
            raise Http404
        else:
            image.delete()
        return HttpResponse('{}', content_type='application/json')

    def image_to_dict(self, image):
        return {
            'id': image.pk,
            'url': image.image.url,
            'order': image.order,
        }

    def handle_image_list(self, request, obj):
        images = []
        for image in obj.images.all():
            data = self.image_to_dict(image)
            if data:
                images.append(data)
        return images, 200

    def handle_image_create(self, request, obj):
        image = obj.images.create(image=request.FILES['image'], order=obj.images.count() + 1)
        return self.image_to_dict(image), 201

    def handle_image_update(self, request, obj):
        data = simplejson.loads(request.raw_post_data)
        for image in data:
            obj.images.filter(pk=image['id']).update(order=image['order'])
        return self.handle_image_list(request, obj)
