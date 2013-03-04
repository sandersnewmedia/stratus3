from django.contrib import admin

from people.models import Person, Team


admin.site.register(Person, list_display=['name'], search_fields=['name'])
admin.site.register(Team)
