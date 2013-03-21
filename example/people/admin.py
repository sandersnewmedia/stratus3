from django.contrib import admin

from people.models import Image, Person, Team


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


admin.site.register(Person, list_display=['name'], search_fields=['name'], inlines=[ImageInline])
admin.site.register(Team)
