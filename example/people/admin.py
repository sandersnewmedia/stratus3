from django.contrib import admin
from django.db import models

from stratus.mixins import OrderableAdminMixin, OrderableTabularInlineMixin
from stratus.widgets import DisplayableImageWidget

from people.models import Image, Person


class ImageInline(OrderableTabularInlineMixin, admin.StackedInline):
    model = Image
    extra = 0
    orderable_field = 'order'
    formfield_overrides = {
        models.ImageField: {
            'widget': DisplayableImageWidget,
        },
    }


class PersonAdmin(OrderableAdminMixin, admin.ModelAdmin):
    list_display = ['name']
    orderable_field = 'order'
    inlines = [ImageInline]


admin.site.register(Person, PersonAdmin)
