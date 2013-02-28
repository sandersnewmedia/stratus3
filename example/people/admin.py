from django.contrib import admin
from django.db import models

from stratus.admin import OrderableModelAdmin, OrderableTabularInline
from stratus.widgets import DisplayableImageWidget

from people.models import Image, Person


class ImageInline(OrderableTabularInline):
    model = Image
    extra = 0
    orderable_field = 'order'
    formfield_overrides = {
        models.ImageField: {'widget': DisplayableImageWidget},
    }


class PersonAdmin(OrderableModelAdmin):
    list_display = ['name']
    orderable_field = 'order'
    inlines = [ImageInline]


admin.site.register(Person, PersonAdmin)
