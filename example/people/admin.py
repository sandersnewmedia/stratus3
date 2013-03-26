from django.contrib import admin

from stratus.admin import OrderableAdmin

from people.models import Image, Person, Team


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class PersonAdmin(OrderableAdmin):
    ordering_field = 'order'
    list_display = ['name', 'order']
    search_fields = ['name']
    inlines = [ImageInline]


admin.site.register(Person, PersonAdmin)
admin.site.register(Team)
